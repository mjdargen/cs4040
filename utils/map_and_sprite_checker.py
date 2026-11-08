"""Check that the Tiled maps and sprites in a project load in Pygame Zero Plus.

Maps: every .tmx map in maps/ is loaded the way a game loads it. Every .tsx
tileset is also checked on its own, by loading a test map that uses each of
its tiles once. This finds missing or misnamed images, tiles that point past
the end of a tileset, and maps that Pygame Zero Plus can't read.

Sprites: the code example in every sprite's .md file in sprites/ (the
Sprite(...) lines that sprite_documenter.py and Sprite Studio write) is run.
This finds sprite sheets that are missing, and frame sizes, rows or frame
counts that don't match the sheet. A frame that comes out completely blank is
reported as something to check: it often means the wrong row or frame count,
but an animation can also end on an empty frame on purpose.

Run it from anywhere; it checks the project folder above utils/, or the
folder you name:

    python map_and_sprite_checker.py                 (Windows)
    python3 map_and_sprite_checker.py                (macOS and Linux)
    python map_and_sprite_checker.py path/to/game    (another project)

Needs Pygame Zero Plus (pip install pgzero-plus).
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Set to True to also check maps/restricted/ and sprites/restricted/, where
# art that can't be shared publicly is kept (those folders aren't committed).
INCLUDE_RESTRICTED = False

SCRIPT_DIR = Path(__file__).resolve().parent
# The project is the folder above utils/, or the folder this script is in
DEFAULT_PROJECT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "utils" else SCRIPT_DIR
TEST_MAP = "_map_and_sprite_checker_test.tmx"

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # no window
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
def package_providing(module_file):
    """The name of the installed package that a module file came from, if pip knows it."""
    from importlib import metadata
    for dist in metadata.distributions():
        for file in dist.files or []:
            if os.path.normcase(str(dist.locate_file(file))) == os.path.normcase(module_file):
                return dist.metadata["Name"]
    return None


try:
    import inspect
    import pygame
    import pgzero
    from pgzero import loaders
    from pgzero.builtins import Actor, Sprite
    from pgzero import tilemaps
except ImportError:
    sys.exit("Pygame Zero Plus isn't installed. Install it with: python -m pip install pgzero-plus")
if "row" not in inspect.signature(Sprite).parameters:
    # An older package that also provides "pgzero" is being imported instead
    old = package_providing(pgzero.__file__) or "an older Pygame Zero"
    sys.exit(
        f"Python is importing pgzero from {old}, at {os.path.dirname(pgzero.__file__)}.\n"
        "That version is older than Pygame Zero Plus: its Sprite has no row= argument.\n"
        f"Uninstall it, then reinstall Pygame Zero Plus:\n"
        f"    python -m pip uninstall {old if old != 'an older Pygame Zero' else 'pgzero'}\n"
        "    python -m pip install --upgrade --force-reinstall pgzero-plus"
    )


def use_folder(loader, subpath):
    """Point a Pygame Zero Plus loader at another folder (such as maps/restricted)."""
    loader._subpath = subpath
    loader._cache.clear()
    loader._have_root = False


def test_map_for(tileset_file):
    """A one-layer map that puts every tile of the tileset down once."""
    tileset = ET.parse(tileset_file).getroot()
    tile_width, tile_height = tileset.get("tilewidth"), tileset.get("tileheight")
    count = int(tileset.get("tilecount", 0))
    columns = int(tileset.get("columns", 0)) or 1
    if count <= 0:
        raise ValueError("it has no tilecount, so it isn't a single-image tileset")
    image = tileset.find("image")
    if image is not None and image.get("width") and image.get("height"):
        # How many tiles the image really holds, the way Tiled counts them
        margin, spacing = int(tileset.get("margin", 0)), int(tileset.get("spacing", 0))
        across = (int(image.get("width")) - margin + spacing) // (int(tile_width) + spacing)
        down = (int(image.get("height")) - margin + spacing) // (int(tile_height) + spacing)
        if columns > across or count > across * down:
            raise ValueError(
                f"it says it has {count} tiles in {columns} columns, but its image "
                f"({image.get('source')}) only holds {across * down} tiles in {across} columns"
            )
    rows = (count + columns - 1) // columns
    gids = [str(i + 1) if i < count else "0" for i in range(columns * rows)]
    data = ",\n".join(",".join(gids[r * columns:(r + 1) * columns]) for r in range(rows))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<map version="1.10" orientation="orthogonal" renderorder="right-down" width="{columns}" '
        f'height="{rows}" tilewidth="{tile_width}" tileheight="{tile_height}" infinite="0">\n'
        f' <tileset firstgid="1" source="{tileset_file.name}"/>\n'
        f' <layer id="1" name="tiles" width="{columns}" height="{rows}"><data encoding="csv">\n'
        f"{data}\n</data></layer>\n</map>\n"
    ), count


def check_maps(folder, subpath):
    """Return (checked, problems) for the maps and tilesets in one folder."""
    if not folder.is_dir():
        return 0, []
    use_folder(loaders.maps, subpath)
    use_folder(loaders.mapimages, subpath)
    checked, problems = 0, []

    for tmx in sorted(folder.glob("*.tmx")):
        if tmx.name == TEST_MAP:
            continue
        checked += 1
        try:
            tilemaps.load_tile_map_actors(tmx.name)
        except Exception as error:
            problems.append(f"{subpath}/{tmx.name}: {error}")

    test_map = folder / TEST_MAP
    try:
        for tsx in sorted(folder.glob("*.tsx")):
            checked += 1
            try:
                text, count = test_map_for(tsx)
                test_map.write_text(text, encoding="utf-8")
                loaders.maps._cache.clear()
                placed = len(tilemaps.load_tile_map_actors(TEST_MAP)["tiles"])
                if placed != count:
                    problems.append(f"{subpath}/{tsx.name}: placed {placed} of its {count} tiles")
            except Exception as error:
                problems.append(f"{subpath}/{tsx.name}: {error}")
    finally:
        if test_map.exists():
            test_map.unlink()
    return checked, problems


def check_sprites(folder, subpath, warnings):
    """Return (checked, problems) for the sprite .md files in one folder.

    Blank frames go in warnings rather than problems: an animation can end on
    an empty frame on purpose, like a character vanishing.
    """
    if not folder.is_dir():
        return 0, []
    use_folder(loaders.sprites, subpath)
    checked, problems = 0, []
    for md in sorted(folder.glob("*.md")):
        if md.name == "README.md":
            continue
        match = re.search(r"```python\n(.*?)```", md.read_text(encoding="utf-8"), re.DOTALL)
        if not match:
            continue
        checked += 1
        names = {"Sprite": Sprite, "Actor": Actor}
        try:
            exec(match.group(1), names)
        except Exception as error:
            problems.append(f"{subpath}/{md.name}: {error}")
            continue
        for variable, value in names.items():
            if isinstance(value, Sprite):
                blank = [i for i, image in enumerate(value.images) if image.get_bounding_rect().width == 0]
                if blank:
                    warnings.append(f"{subpath}/{md.name}: {variable} has blank frames {blank}")
    return checked, problems


def main():
    project = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_PROJECT
    if not project.is_dir():
        sys.exit(f"There's no folder called {project}.")
    pygame.init()
    pygame.display.set_mode((1, 1))
    loaders.set_root(str(project))

    folders = ["maps", "sprites"]
    if INCLUDE_RESTRICTED:
        folders += ["maps/restricted", "sprites/restricted"]
    total, all_problems, warnings = 0, [], []
    for subpath in folders:
        if subpath.startswith("maps"):
            checked, problems = check_maps(project / subpath, subpath)
        else:
            checked, problems = check_sprites(project / subpath, subpath, warnings)
        if checked:
            print(f"{subpath}: checked {checked} files, {len(problems)} problem(s)")
        total += checked
        all_problems += problems

    for problem in all_problems:
        print("  Problem: " + problem)
    for warning in warnings:
        print("  Check this (may be on purpose): " + warning)
    if all_problems:
        sys.exit(f"{len(all_problems)} problem(s) in {total} files.")
    print(f"Everything loads: {total} files checked.")


if __name__ == "__main__":
    main()
