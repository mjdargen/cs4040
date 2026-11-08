"""Make sure every sprite in the sprites folder has a .png sheet, an .aseprite
file and .md notes, and write sprites/README.md linking to them all.

For each sprite:

- .aseprite only: the .png sheet is exported from it, one animation (tag) per
  row, the way Sprite Studio (https://dargen.io/sprite-studio/) lays them out.
  Frames that aren't in a tag are left out. A file with no tags is one row.
- .png only: an .aseprite file is made from it, with a tag for each
  animation, so it can be edited in Aseprite. The animations come from the
  sheet's .md notes if it has them (from Sprite Studio or an earlier run).
  Without notes, the frame size comes from FRAME_SIZES below, or else it is
  guessed (the same way Sprite Studio guesses) and you're asked to confirm it
  and name each row. Each row becomes a tag, without the empty frames at the
  end of the row. When it can't ask (not run in a terminal), the sheet is
  skipped.
- Both: the .aseprite file is exported and compared with the .png. If they
  don't match, one was changed without the other, so that sprite is left
  alone and a warning asks which one is up to date.
- Then the .md notes are written from the .aseprite file: the sheet's size,
  the frame size, each animation's row and frame count, and example code that
  makes a Sprite for each animation. A "## Asset credits" section already in
  the README is kept.

Run it from anywhere; it works on the project's sprites folder, or on the
folder you name:

    python sprite_documenter.py                  (Windows)
    python3 sprite_documenter.py                 (macOS and Linux)
    python sprite_documenter.py path/to/folder   (another folder of sprites)

Needs Aseprite (https://www.aseprite.org), Pillow and numpy.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw

# The scripts in utils/ always work on the project folder above them
PROJECT_DIR = Path(__file__).resolve().parent.parent
SPRITES_DIR = PROJECT_DIR / "sprites"

# Set to True to also do sprites/restricted/ (that folder isn't committed).
# It gets its own README.
INCLUDE_RESTRICTED = False
RESTRICTED_DIR = SPRITES_DIR / "restricted"

# Frame sizes for .png sheets that have no .aseprite file and no .md notes,
# e.g. {"hero": (24, 16)}. Sheets that aren't listed get a guessed size to
# confirm. Their rows are called row0, row1 and so on.
FRAME_SIZES = {}

# Frames per second written into the code examples, and used for the frames
# of .aseprite files made from sheets whose notes don't give a speed
FPS = 5

# Where Aseprite is usually installed, if it isn't on the PATH
ASEPRITE_LOCATIONS = [
    "C:/Program Files/Aseprite/Aseprite.exe",
    "C:/Program Files (x86)/Steam/steamapps/common/Aseprite/Aseprite.exe",
    "/Applications/Aseprite.app/Contents/MacOS/aseprite",
    "~/Library/Application Support/Steam/steamapps/common/Aseprite/Aseprite.app/Contents/MacOS/aseprite",
    "~/.steam/steam/steamapps/common/Aseprite/aseprite",
    "~/.local/share/Steam/steamapps/common/Aseprite/aseprite",
]

# Reading .md notes (this script's and Sprite Studio's look the same)
ANIMATION_LINE = re.compile(r"^- (.+) - row (\d+) - (\d+) frames?$", re.MULTILINE)
FRAME_SIZE_LINE = re.compile(r"\*\*Frame Size:\*\* (\d+)x(\d+)")
SPRITE_LINE = re.compile(r"Sprite\(.*?row=(\d+).*?fps=([\d.]+)(.*?)\)")

# Runs inside Aseprite to make .aseprite files from sheets: cuts each frame out
# of the sheet, then adds the tags
MAKE_ASEPRITE_LUA = """
local file = io.open(app.params.jobs)
local jobs = json.decode(file:read("a"))
file:close()
for _, job in ipairs(jobs) do
  local sheet = Image{ fromFile = job.png }
  local across = sheet.width // job.width
  local sprite = Sprite(job.width, job.height, ColorMode.RGB)
  local layer = sprite.layers[1]
  local count = 0
  local spans = {}
  for _, animation in ipairs(job.animations) do
    local first = count + 1
    for i = 0, animation.frames - 1 do
      local cell = animation.row * across + i  -- frames can carry on into the next row
      local frame = Image(job.width, job.height, ColorMode.RGB)
      frame:drawImage(sheet, Point(-(cell % across) * job.width, -(cell // across) * job.height))
      count = count + 1
      if count > 1 then sprite:newEmptyFrame() end
      sprite:newCel(layer, count, frame, Point(0, 0))
      sprite.frames[count].duration = 1 / animation.fps
    end
    table.insert(spans, { animation, first, count })
  end
  -- Tags go on after every frame exists: Aseprite stretches a tag that ends on
  -- the last frame whenever another frame is added after it
  for _, span in ipairs(spans) do
    local tag = sprite:newTag(span[2], span[3])
    tag.name = span[1].name
    if not span[1].loop then tag.repeats = 1 end
  end
  sprite:saveAs(job.aseprite)
  sprite:close()
end
"""


def find_aseprite():
    for name in ("aseprite", "Aseprite"):
        found = shutil.which(name)
        if found:
            return found
    for location in ASEPRITE_LOCATIONS:
        path = Path(location).expanduser()
        if path.is_file():
            return str(path)
    sys.exit(
        "Couldn't find Aseprite. Install it from https://www.aseprite.org, or add the "
        "folder it's in to your PATH."
    )


def to_snake_case(name):
    """Running Left -> running_left, runLeft -> run_left"""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^a-z0-9]+", "_", name.lower())
    return name.strip("_")


# ---- .png only: make the .aseprite file ----

def animations_from_notes(md_path):
    """The frame size and animations in a sprite's .md notes, or None."""
    text = md_path.read_text(encoding="utf-8")
    size = FRAME_SIZE_LINE.search(text)
    animations = ANIMATION_LINE.findall(text)
    if not size or not animations:
        return None
    speeds = {int(row): (float(fps), "loop=False" not in rest) for row, fps, rest in SPRITE_LINE.findall(text)}
    return (int(size.group(1)), int(size.group(2))), [
        {"name": name, "row": int(row), "frames": int(frames),
         "fps": speeds.get(int(row), (FPS, True))[0], "loop": speeds.get(int(row), (FPS, True))[1]}
        for name, row, frames in animations
    ]


def animations_from_rows(sheet_path, width, height):
    """One animation per row, without the empty frames at the end of each row."""
    sheet = Image.open(sheet_path).convert("RGBA")
    animations = []
    for row in range(sheet.height // height):
        frames = [sheet.crop((x, row * height, x + width, (row + 1) * height)).getbbox()
                  for x in range(0, sheet.width - width + 1, width)]
        used = max((i + 1 for i, box in enumerate(frames) if box), default=0)
        if used:
            animations.append({"name": "row{}".format(row), "row": row, "frames": used, "fps": FPS, "loop": True})
    return animations


# ---- .png with no notes: guess the frame size, then ask ----

def guess_frame_size(sheet_path):
    """A guess at a sheet's frame size: (width, height).

    The same guess Sprite Studio makes (js/core/grid.js in sprite-studio).
    Most sheets leave a little space around each character, so the lines
    between real frames have much less art crossing them than a typical line.
    Along each side, the guess is the smallest size (at least 8 pixels,
    dividing the side into 2 or more frames) whose lines have less than a
    third of the typical amount. Its multiples pass too, which is why the
    smallest wins. If neither side has such a size, a strip of square frames
    is next most likely, and then the whole image as one frame.
    """
    pixels = np.asarray(Image.open(sheet_path).convert("RGBA")).astype(np.int16)
    # Art is anything that isn't see-through or the solid background color in the top-left corner
    background = pixels[..., 3] == 0
    corner = pixels[0, 0]
    if corner[3] == 255:
        background |= np.all(pixels[..., :3] == corner[:3], axis=-1)
    art = ~background
    height, width = art.shape
    # How much art crosses the line before each column and each row (0 to 1)
    across_columns = np.zeros(width)
    across_columns[1:] = (art[:, 1:] & art[:, :-1]).sum(axis=0) / height
    across_rows = np.zeros(height)
    across_rows[1:] = (art[1:, :] & art[:-1, :]).sum(axis=1) / width

    def size_along(length, crossed):
        typical = crossed[1:].mean() if length > 1 else 0
        if typical == 0:
            return length
        for size in range(8, length // 2 + 1):
            if length % size == 0 and crossed[size::size][:length // size - 1].mean() < typical / 3:
                return size
        return length

    frame_width, frame_height = size_along(width, across_columns), size_along(height, across_rows)
    if (frame_width, frame_height) != (width, height):
        return frame_width, frame_height
    if width > height and width % height == 0:
        return height, height
    if height > width and height % width == 0:
        return width, width
    return width, height


def show_grid(sheet_path, width, height):
    """Open a picture of the sheet with the frame lines drawn on it."""
    sheet = Image.open(sheet_path).convert("RGBA")
    scale = max(1, min(8, 1000 // max(sheet.size)))
    picture = Image.new("RGBA", sheet.size, (60, 60, 70, 255))
    picture.alpha_composite(sheet)
    picture = picture.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST)
    draw = ImageDraw.Draw(picture)
    for x in range(0, picture.width, width * scale):
        draw.line([(x, 0), (x, picture.height)], fill=(255, 0, 0, 255))
    for y in range(0, picture.height, height * scale):
        draw.line([(0, y), (picture.width, y)], fill=(255, 0, 0, 255))
    path = Path(tempfile.gettempdir()) / "{}_grid.png".format(sheet_path.stem)
    picture.save(path)
    if sys.platform == "win32":
        os.startfile(path)
    else:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)])
    print("  Opened {}".format(path))


def ask_for_layout(sheet_path):
    """Guess a sheet's frame size, then let the person running this confirm or change it,
    and name the animations. Returns ((width, height), animations), or None to skip it."""
    with Image.open(sheet_path) as sheet:
        sheet_width, sheet_height = sheet.size
    width, height = guess_frame_size(sheet_path)
    print("\n{} ({}x{}) has no .aseprite file or .md notes.".format(sheet_path.name, sheet_width, sheet_height))
    while True:
        animations = animations_from_rows(sheet_path, width, height)
        print("  It looks like {}x{} frames, {} across and {} down.".format(
            width, height, sheet_width // width, sheet_height // height))
        if sheet_width % width or sheet_height % height:
            print("  ({} pixels on the right and {} at the bottom aren't in any frame.)".format(
                sheet_width % width, sheet_height % height))
        print("  Frames in each row: {}".format(", ".join(str(a["frames"]) for a in animations) or "none"))
        answer = input("  Press Enter to use this, type another size (like 32x32), "
                       "p to see the grid, or s to skip: ").strip().lower()
        if answer == "":
            break
        if answer == "s":
            return None
        if answer == "p":
            show_grid(sheet_path, width, height)
            continue
        size = re.fullmatch(r"(\d+)\s*[x*, ]\s*(\d+)", answer)
        if size and 0 < int(size.group(1)) <= sheet_width and 0 < int(size.group(2)) <= sheet_height:
            width, height = int(size.group(1)), int(size.group(2))
        else:
            print("  That isn't a frame size that fits, like 32x32.")
    if not animations:
        return (width, height), animations

    while True:
        answer = input("  Names for the {} animations, top row first, separated by commas "
                       "(Enter for row0, row1, ...): ".format(len(animations))).strip()
        if not answer:
            break
        names = [name.strip() for name in answer.split(",")]
        if len(names) != len(animations) or "" in names:
            print("  That's {} names; it needs {}.".format(len([n for n in names if n]), len(animations)))
        elif len({to_snake_case(name) for name in names}) != len(names):
            print("  Each animation needs a different name.")
        else:
            for animation, name in zip(animations, names):
                animation["name"] = name
            break
    return (width, height), animations


def make_aseprite_files(aseprite, sheets):
    """Make an .aseprite file for each .png sheet that can be worked out."""
    jobs = []
    for sheet_path in sheets:
        notes = sheet_path.with_suffix(".md")
        found = animations_from_notes(notes) if notes.exists() else None
        if found:
            (width, height), animations = found
        elif sheet_path.stem in FRAME_SIZES:
            width, height = FRAME_SIZES[sheet_path.stem]
            animations = animations_from_rows(sheet_path, width, height)
        elif sys.stdin.isatty():
            try:
                layout = ask_for_layout(sheet_path)
            except (EOFError, KeyboardInterrupt):
                print()
                layout = None
            if layout is None:
                print("Skipped {}.".format(sheet_path.name))
                continue
            (width, height), animations = layout
        else:
            print("Skipped {}: it has no .aseprite file or .md notes, so its frame size isn't known. "
                  "Run this in a terminal to be asked, or add it to FRAME_SIZES.".format(sheet_path.name))
            continue
        if not animations:
            print("Skipped {}: no frames found.".format(sheet_path.name))
            continue
        jobs.append({"png": sheet_path, "aseprite": sheet_path.with_suffix(".aseprite").as_posix(),
                     "width": width, "height": height, "animations": animations})
    if not jobs:
        return

    with tempfile.TemporaryDirectory() as tmp:
        # Aseprite gets an RGBA copy of each sheet: it doesn't keep the
        # transparent color of palette (indexed) PNGs when copying their frames
        for number, job in enumerate(jobs):
            copy = Path(tmp) / "sheet{}.png".format(number)
            Image.open(job["png"]).convert("RGBA").save(copy)
            job["png"] = copy.as_posix()
        jobs_file, script = Path(tmp) / "jobs.json", Path(tmp) / "make_aseprite.lua"
        jobs_file.write_text(json.dumps(jobs), encoding="utf-8")
        script.write_text(MAKE_ASEPRITE_LUA, encoding="utf-8")
        result = subprocess.run([aseprite, "-b", "--script-param", "jobs=" + str(jobs_file),
                                 "--script", str(script)], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Aseprite couldn't make the .aseprite files. {}".format((result.stderr or result.stdout).strip()))
    for job in jobs:
        if Path(job["aseprite"]).exists():
            print("Made {}".format(Path(job["aseprite"]).name))


# ---- .aseprite only: export the .png sheet ----

def render_sheet(aseprite, file_path, metadata):
    """The sheet an .aseprite file should have: one row per tag, in tag order.

    Frames that aren't in any tag are left out. (Aseprite's own "split tags"
    export puts them in an extra row before the tags, which would put every
    animation one row off from its notes.) A file with no tags is one row.
    Returns None if Aseprite couldn't export the frames.
    """
    with tempfile.TemporaryDirectory() as tmp:
        strip_path = Path(tmp) / "frames.png"
        command = [aseprite, "-b", str(file_path), "--sheet", str(strip_path), "--sheet-type", "horizontal"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0 or not strip_path.exists():
            print("  Error: Aseprite couldn't export {}. {}".format(file_path.name, result.stderr.strip()))
            return None
        strip = Image.open(strip_path).convert("RGBA")
    first_frame = next(iter(metadata["frames"].values()))["frame"]
    width, height = first_frame["w"], first_frame["h"]
    tags = metadata["meta"].get("frameTags") or [{"from": 0, "to": len(metadata["frames"]) - 1}]
    rows = [list(range(min(t["from"], t["to"]), max(t["from"], t["to"]) + 1)) for t in tags]
    sheet = Image.new("RGBA", (max(len(r) for r in rows) * width, len(rows) * height), (0, 0, 0, 0))
    for row, frames in enumerate(rows):
        for column, frame in enumerate(frames):
            cell = strip.crop((frame * width, 0, (frame + 1) * width, height))
            sheet.paste(cell, (column * width, row * height))
    return sheet


# ---- both: check they agree ----

def comparable(image):
    """RGBA, with every see-through pixel the same, so only visible pixels count."""
    image = image.convert("RGBA")
    visible = image.getchannel("A").point(lambda alpha: 255 if alpha else 0)
    return Image.composite(image, Image.new("RGBA", image.size, (0, 0, 0, 0)), visible)


def sheet_matches(rendered, sheet_path):
    """Whether the .png is the sheet the .aseprite file makes. Extra empty space doesn't count."""
    exported = comparable(rendered)
    with Image.open(sheet_path) as sheet:
        existing = comparable(sheet)
    size = (max(exported.width, existing.width), max(exported.height, existing.height))
    padded = []
    for image in (exported, existing):
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        canvas.paste(image, (0, 0))
        padded.append(canvas)
    return ImageChops.difference(*padded).getbbox() is None


def saved_at(path):
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


# ---- the notes ----

def extract_metadata(aseprite, file_path):
    """Get the frames and tags (animations) of an Aseprite file."""
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.json"
        command = [aseprite, "-b", "--list-tags", "--data", str(data_file), str(file_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0 or not data_file.exists():
            print("  Error: Aseprite couldn't read it. {}".format(result.stderr.strip()))
            return None
        with open(data_file, encoding="utf-8") as f:
            return json.load(f)


def generate_documentation(metadata, sheet_path, output_file):
    """Write the .md file for one sprite. Return False if it couldn't."""
    first_frame = next(iter(metadata["frames"].values()))
    frame_width = first_frame["frame"]["w"]
    frame_height = first_frame["frame"]["h"]
    tags = metadata["meta"].get("frameTags", [])
    animations = [{"name": tag["name"], "frames": abs(tag["from"] - tag["to"]) + 1,
                   "loop": "repeat" not in tag} for tag in tags]
    if not animations:
        # No tags: every frame is one animation, exported as one row
        animations = [{"name": "default", "frames": len(metadata["frames"]), "loop": True}]

    # The size of the sprite sheet the game loads, not Aseprite's own layout
    with Image.open(sheet_path) as sheet:
        sheet_width, sheet_height = sheet.size
    columns = sheet_width // frame_width
    rows = sheet_height // frame_height
    if len(animations) > rows:
        print("  Warning: {} animations, but {} only has {} rows of {}-pixel frames.".format(
            len(animations), sheet_path.name, rows, frame_height))
    for row, animation in enumerate(animations):
        if animation["frames"] > columns:
            print("  Warning: '{}' has {} frames, but {} only fits {} across.".format(
                animation["name"], animation["frames"], sheet_path.name, columns))

    name = output_file.stem
    sprite_name = to_snake_case(name)
    lines = [
        "# {}.aseprite".format(name),
        "**Image Size:** {}x{}\n".format(sheet_width, sheet_height),
        "**Frame Size:** {}x{}\n".format(frame_width, frame_height),
        "**Number of Animations:** {}\n".format(len(animations)),
        "**Animations:**",
    ]
    for row, animation in enumerate(animations):
        lines.append("- {} - row {} - {} frames".format(animation["name"], row, animation["frames"]))
    lines += ["", "**Code Example:**", "```python", "# Note: fps is set to {} below; adjust as needed".format(FPS)]
    for row, animation in enumerate(animations):
        lines.append(
            '{}_{} = Sprite("{}", frame_width={}, frame_height={}, row={}, frames={}, fps={}{})'.format(
                sprite_name, to_snake_case(animation["name"]), name, frame_width, frame_height, row,
                animation["frames"], FPS, "" if animation["loop"] else ", loop=False"))
    lines += ["", "# Define the Actor", "{} = Actor({}_{})".format(
        sprite_name, sprite_name, to_snake_case(animations[0]["name"]))]
    lines.append("```")

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  Wrote {}".format(output_file.name))
    return True


def generate_readme(directory):
    """Write README.md, linking to every sprite's .md file."""
    markdown_files = sorted(p.name for p in directory.glob("*.md") if p.name != "README.md")
    lines = [
        "# Sprite Documentation",
        "",
        "This folder contains some example sprites that you can use for your projects. The `.png` files "
        "are the spritesheets you will use in your project. The `.md` files (also linked below) provide "
        "dimensions and information about each of the animations in the sprite. The `.aseprite` files "
        "are the source files used to create the sprites.",
        "",
        "Read the `.md` files first by clicking the links for the sprite you want below. Each file "
        "provides metadata about the sprite, a breakdown of animations, and example usage code.",
        "",
        "After adding or changing sprites, run `python utils/map_and_sprite_checker.py` from the "
        "repository folder to check that everything loads in Pygame Zero Plus.",
        "",
        "## Sprite Documentation Files",
        "",
    ]
    if markdown_files:
        lines += ["- [{}]({})".format(Path(md).stem, md) for md in markdown_files]
    else:
        lines.append("No sprite documentation files have been generated yet.")

    # Keep the hand-written credits section, if the README already has one
    readme = directory / "README.md"
    credits_heading = "## Asset credits"
    if readme.exists():
        old = readme.read_text(encoding="utf-8")
        if credits_heading in old:
            lines += ["", old[old.index(credits_heading):].rstrip("\n")]
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote README.md")


def process_all_files(directory):
    aseprite = find_aseprite()

    # .png only: make the .aseprite file first, so the notes can be written from it
    sheets_only = [p for p in sorted(directory.glob("*.png")) if not p.with_suffix(".aseprite").exists()]
    make_aseprite_files(aseprite, sheets_only)

    aseprite_files = sorted(directory.glob("*.aseprite"))
    if not aseprite_files:
        print("No .aseprite files found in {}.".format(directory))
        return
    disagree = []
    for file_path in aseprite_files:
        print("Processing {}...".format(file_path.name))
        metadata = extract_metadata(aseprite, file_path)
        if metadata is None:
            continue
        sheet_path = file_path.with_suffix(".png")
        rendered = render_sheet(aseprite, file_path, metadata)
        if rendered is None:
            continue
        if not sheet_path.exists():
            # .aseprite only: export the .png sheet
            rendered.save(sheet_path)
            print("  Exported {}".format(sheet_path.name))
        elif not sheet_matches(rendered, sheet_path):
            # Both, but one was changed without the other: don't guess which is right
            print("  Skipped: {} and {} don't match, so nothing was changed.".format(file_path.name, sheet_path.name))
            disagree.append((file_path, sheet_path))
            continue
        generate_documentation(metadata, sheet_path, file_path.with_suffix(".md"))

    generate_readme(directory)

    for file_path, sheet_path in disagree:
        print("\nWarning: {} and {} don't match. Which one is up to date?".format(file_path.name, sheet_path.name))
        print("  {} was saved {}, and {} was saved {}.".format(
            file_path.name, saved_at(file_path), sheet_path.name, saved_at(sheet_path)))
        print("  If the .aseprite file is, delete {} and run this again to export it.".format(sheet_path.name))
        print("  If the .png is, delete {} and run this again to make it from the .png "
              "(check its .md notes still describe the .png).".format(file_path.name))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folders = [Path(sys.argv[1]).resolve()]
    else:
        folders = [SPRITES_DIR]
        if INCLUDE_RESTRICTED and RESTRICTED_DIR.is_dir():
            folders.append(RESTRICTED_DIR)
    for folder in folders:
        if not folder.is_dir():
            sys.exit("There's no folder called {}.".format(folder))
        print("Documenting {}...".format(folder))
        process_all_files(folder)
    print("Done.")
