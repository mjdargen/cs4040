"""Write a .md file for each Aseprite sprite in the sprites folder.

Each .md file gives the sprite sheet's size, frame size and animations, and
example code that makes a Sprite for each animation. It also writes
sprites/README.md, which links to them all.

It expects each .aseprite file to have been exported next to it as a .png
sprite sheet with one animation (tag) per row, the way spritesheet_creator.py
lays them out.

Needs Aseprite (https://www.aseprite.org) and Pillow.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

# The scripts in utils/ always work on the project folder above them
PROJECT_DIR = Path(__file__).resolve().parent.parent
SPRITES_DIR = PROJECT_DIR / "sprites"

# Where Aseprite is usually installed, if it isn't on the PATH
ASEPRITE_LOCATIONS = [
    "C:/Program Files/Aseprite/Aseprite.exe",
    "C:/Program Files (x86)/Steam/steamapps/common/Aseprite/Aseprite.exe",
    "/Applications/Aseprite.app/Contents/MacOS/aseprite",
    "~/Library/Application Support/Steam/steamapps/common/Aseprite/Aseprite.app/Contents/MacOS/aseprite",
    "~/.steam/steam/steamapps/common/Aseprite/aseprite",
    "~/.local/share/Steam/steamapps/common/Aseprite/aseprite",
]


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
    animations = [{"name": tag["name"], "frames": abs(tag["from"] - tag["to"]) + 1} for tag in tags]

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
    lines += ["", "**Code Example:**", "```python", "# Note: fps is set to 5 below; adjust as needed"]
    for row, animation in enumerate(animations):
        lines.append(
            '{}_{} = Sprite("{}", frame_width={}, frame_height={}, row={}, frames={}, fps=5)'.format(
                sprite_name, to_snake_case(animation["name"]), name, frame_width, frame_height, row,
                animation["frames"]))
    if animations:
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
        "## Sprite Documentation Files",
        "",
    ]
    if markdown_files:
        lines += ["- [{}]({})".format(Path(md).stem, md) for md in markdown_files]
    else:
        lines.append("No sprite documentation files have been generated yet.")
    (directory / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote README.md")


def process_all_files(directory):
    aseprite_files = sorted(directory.glob("*.aseprite"))
    if not aseprite_files:
        print("No .aseprite files found in {}.".format(directory))
        return
    aseprite = find_aseprite()

    for file_path in aseprite_files:
        print("Processing {}...".format(file_path.name))
        sheet_path = file_path.with_suffix(".png")
        if not sheet_path.exists():
            print("  Skipped: there's no {}. Export the sprite sheet from Aseprite first.".format(sheet_path.name))
            continue
        metadata = extract_metadata(aseprite, file_path)
        if metadata is not None:
            generate_documentation(metadata, sheet_path, file_path.with_suffix(".md"))

    generate_readme(directory)


if __name__ == "__main__":
    process_all_files(SPRITES_DIR)
    print("Done.")
