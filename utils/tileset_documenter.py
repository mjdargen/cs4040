"""Write the tileset tables in maps/README.md from the .tsx files.

Every .tsx tileset in the maps folder gets a row in its style's table, read
straight from the file: tile width, tile height, grid (columns x rows), image
size, and any spacing or margin between tiles. Tilesets whose names start with
platformer_ go under "## Platformer tilesets"; topdown_ ones go under
"## Top-down tilesets".

Only the tables are rewritten. Everything else in the README, including the
notes under each table, is kept as it is. A section that doesn't have a table
yet gets one right under its heading.

It also sets Tile Render Size to Map Grid Size (tilerendersize="grid") on
every .tsx, so Tiled draws each tile at the map's tile size instead of the
tileset's, the way Pygame Zero Plus does in the game. Fill Mode is left on
Stretch (Tiled's default), which also matches the game: a tile fills its whole
square, even if that stretches it. Any other fill mode is removed.

And it warns when a .tsx file's image size doesn't match its .png, or when
the image size doesn't divide evenly into tiles.

Run it from anywhere; it works on the project's maps folder, or on the folder
you name:

    python tileset_documenter.py                  (Windows)
    python3 tileset_documenter.py                 (macOS and Linux)
    python tileset_documenter.py path/to/folder   (another folder of tilesets)
"""
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# The scripts in utils/ always work on the project folder above them
PROJECT_DIR = Path(__file__).resolve().parent.parent
MAPS_DIR = PROJECT_DIR / "maps"

# Which README heading each tileset name prefix goes under
SECTIONS = {
    "platformer_": "## Platformer tilesets",
    "topdown_": "## Top-down tilesets",
}

# Tiled options set on every tileset, in the order Tiled writes them.
# None removes the option, so Tiled uses its default (fillmode: Stretch).
RENDER_SETTINGS = {
    "tilerendersize": "grid",
    "fillmode": None,
}

HEADER = [
    "| Tileset | Tile width | Tile height | Grid (cols × rows) | Image size | Notes |",
    "|---|---|---|---|---|---|",
]


def png_size(path):
    """The (width, height) of a .png file, read from its header."""
    with open(path, "rb") as file:
        data = file.read(24)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def set_render_settings(tsx):
    """Set RENDER_SETTINGS on the .tsx's <tileset> tag. Return True if it changed.

    Edits the text rather than rewriting the XML, so the file stays exactly
    the way Tiled saved it apart from these attributes.
    """
    with open(tsx, encoding="utf-8", newline="") as file:
        text = file.read()
    match = re.search(r"<tileset\b[^>]*?(/?)>", text)
    if not match:
        return False
    tag = match.group(0)
    end = len(tag) - (2 if match.group(1) else 1)
    new_tag = tag[:end]
    for name, value in RENDER_SETTINGS.items():
        new_tag = re.sub(rf'\s{name}="[^"]*"', "", new_tag)
        if value is not None:
            new_tag += f' {name}="{value}"'
    new_tag += tag[end:]
    if new_tag == tag:
        return False
    with open(tsx, "w", encoding="utf-8", newline="") as file:
        file.write(text.replace(tag, new_tag, 1))
    return True


def read_tileset(tsx):
    """Return a dict describing one .tsx tileset, and a list of warnings."""
    root = ET.parse(tsx).getroot()
    image = root.find("image")
    info = {
        "name": tsx.stem,
        "tile_width": int(root.get("tilewidth")),
        "tile_height": int(root.get("tileheight")),
        "columns": int(root.get("columns", 0)),
        "count": int(root.get("tilecount", 0)),
        "spacing": int(root.get("spacing", 0)),
        "margin": int(root.get("margin", 0)),
        "image_width": int(image.get("width")) if image is not None else 0,
        "image_height": int(image.get("height")) if image is not None else 0,
    }
    warnings = []
    if image is None:
        warnings.append(f"{tsx.name}: no single image (collection of images?)")
        return info, warnings

    png = tsx.parent / image.get("source")
    if not png.exists():
        warnings.append(f"{tsx.name}: image {image.get('source')} is missing")
    else:
        size = png_size(png)
        if size and size != (info["image_width"], info["image_height"]):
            warnings.append(
                f"{tsx.name}: says the image is {info['image_width']}×{info['image_height']}, "
                f"but {png.name} is {size[0]}×{size[1]}"
            )

    # The image should be margin + tiles + spacing between them + margin
    width_used = 2 * info["margin"] + info["columns"] * info["tile_width"] + (info["columns"] - 1) * info["spacing"]
    if info["columns"] and width_used != info["image_width"]:
        warnings.append(f"{tsx.name}: {info['columns']} columns of tiles don't fill the image width exactly")
    return info, warnings


def table_row(info):
    """One Markdown table row for a tileset."""
    rows = info["count"] // info["columns"] if info["columns"] else 0
    notes = []
    if info["spacing"]:
        notes.append(f"{info['spacing']} px spacing between tiles")
    if info["margin"]:
        notes.append(f"{info['margin']} px margin around the edge")
    cells = [
        f"`{info['name']}`",
        f"{info['tile_width']} px",
        f"{info['tile_height']} px",
        f"{info['columns']} × {rows}",
        f"{info['image_width']} × {info['image_height']}",
        ", ".join(notes),
    ]
    return "| " + " | ".join(cells).rstrip() + " |"


def replace_table(lines, heading, rows):
    """Put a fresh table under heading, replacing the first table in that section."""
    if heading not in lines:
        print(f"README has no '{heading}' section, so those tilesets were left out")
        return lines
    start = lines.index(heading) + 1
    # The section ends at the next heading of the same or higher level
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    table = HEADER + rows

    first = next((i for i in range(start, end) if lines[i].startswith("|")), None)
    if first is None:
        return lines[:start] + [""] + table + lines[start:]
    last = first
    while last + 1 < end and lines[last + 1].startswith("|"):
        last += 1
    return lines[:first] + table + lines[last + 1:]


def main():
    folder = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else MAPS_DIR
    readme = folder / "README.md"
    if not readme.exists():
        print(f"No README.md in {folder}")
        return

    rows = {heading: [] for heading in SECTIONS.values()}
    all_warnings = []
    changed = [tsx.name for tsx in sorted(folder.glob("*.tsx")) if set_render_settings(tsx)]
    if changed:
        print(f"Set Map Grid Size (and Stretch) in {len(changed)} tilesets: {', '.join(changed)}")
    for tsx in sorted(folder.glob("*.tsx")):
        heading = next((h for prefix, h in SECTIONS.items() if tsx.name.startswith(prefix)), None)
        if heading is None:
            all_warnings.append(f"{tsx.name}: name doesn't start with platformer_ or topdown_, so it isn't listed")
            continue
        info, warnings = read_tileset(tsx)
        all_warnings += warnings
        rows[heading].append(table_row(info))

    lines = readme.read_text(encoding="utf-8").splitlines()
    for heading, section_rows in rows.items():
        if section_rows:
            lines = replace_table(lines, heading, section_rows)
    with open(readme, "w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines) + "\n")

    count = sum(len(r) for r in rows.values())
    print(f"Wrote {count} tilesets to {readme.relative_to(folder.parent)}")
    for warning in all_warnings:
        print("Warning:", warning)


if __name__ == "__main__":
    main()
