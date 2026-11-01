"""Move Tiled maps, and the tilesets and images they use, into the maps folder.

Pygame Zero Plus loads maps from the maps folder, so a map saved in Downloads,
or one whose tileset image is still in Downloads, can't be found. This finds
the maps in the project folder, the maps folder, Downloads and the Desktop,
moves them and everything they use into maps, and fixes the paths in them.

It shows what it will do and asks before changing anything:

    python resolve_tilemaps.py          (Windows)
    python3 resolve_tilemaps.py         (macOS and Linux)

Add --yes to skip the question.
"""
import argparse
import filecmp
import os
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# The project is the folder this script is in, or the one above utils/
PROJECT_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "utils" else SCRIPT_DIR
MAPS_DIR = PROJECT_DIR / "maps"
# Other places where students often save maps and tilesets
OTHER_PLACES = [Path.home() / "Downloads", Path.home() / "Desktop"]
# Files in these project folders may also be used by the game, so they are
# copied into maps instead of moved
GAME_FOLDERS = ["images", "sprites", "sounds", "music", "fonts"]


def main():
    parser = argparse.ArgumentParser(description="Move Tiled maps and what they use into the maps folder.")
    parser.add_argument("--yes", action="store_true", help="don't ask before moving files")
    args = parser.parse_args()

    print("Project folder: {}".format(PROJECT_DIR))
    plan = Plan()
    for tmx in find_maps():
        plan.add_file(tmx)

    if not plan.moves and not plan.copies and not plan.path_fixes() and not plan.missing:
        print("Everything is already in the maps folder.")
        return
    plan.show()
    if not plan.moves and not plan.copies and not plan.path_fixes():
        return
    if not args.yes:
        answer = input("\nGo ahead? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Nothing was changed.")
            return
    plan.carry_out()


def find_maps():
    """The .tmx files in the project folder, maps folder, Downloads and Desktop."""
    maps = list(PROJECT_DIR.glob("*.tmx"))
    if MAPS_DIR.is_dir():
        maps += MAPS_DIR.rglob("*.tmx")
    for place in OTHER_PLACES:
        if place.is_dir():
            maps += place.glob("*.tmx")
    return sorted(set(p.resolve() for p in maps))


def short(path):
    """`path` written short, e.g. ~/Downloads/tiles.png, for printing."""
    for base, start in [(PROJECT_DIR.resolve(), ""), (Path.home().resolve(), "~/")]:
        if is_inside(path, base):
            return start + path.relative_to(base).as_posix()
    return str(path)


def is_inside(path, folder):
    try:
        path.relative_to(folder)
        return True
    except ValueError:
        return False


class Plan:
    """Work out where every file goes before changing anything."""

    def __init__(self):
        self.destinations = {}  # file -> where it will be
        self.moves = []  # (from, to)
        self.copies = []  # (from, to)
        self.trees = {}  # .tmx/.tsx file -> parsed XML
        self.references = []  # (owner file, element, attribute, target file)
        self.missing = []  # (owner file, path written in it)

    def add_file(self, path):
        """Plan where `path` goes, and follow the files it refers to."""
        if path in self.destinations:
            return
        self.destinations[path] = self.choose_destination(path)

        if path.suffix.lower() not in (".tmx", ".tsx"):
            return
        try:
            tree = ET.parse(str(path))
        except ET.ParseError as error:
            print("Skipping {}: it isn't a valid Tiled file ({}).".format(path, error))
            return
        self.trees[path] = tree
        for element in tree.getroot().iter():
            # tileset: a separate .tsx file. image: a tileset's image, a tile's
            # image in an image-collection tileset, or an image layer.
            if element.tag in ("tileset", "image") and element.get("source"):
                written = element.get("source")
                target = self.find_reference(path, written)
                if target is None:
                    self.missing.append((path, written))
                    continue
                self.references.append((path, element, target))
                self.add_file(target)

    def find_reference(self, owner, written):
        """Find the file that `written`, a path in `owner`, means."""
        direct = owner.parent / written
        if direct.is_file():
            return direct.resolve()
        # Not where the path says (e.g. a path from another computer, or the
        # file was moved). Look for a file with the same name nearby.
        name = Path(written.replace("\\", "/")).name
        places = [owner.parent, MAPS_DIR] + OTHER_PLACES
        for place in places:
            if (place / name).is_file():
                return (place / name).resolve()
        for place in [MAPS_DIR] + OTHER_PLACES:
            if place.is_dir():
                for match in place.rglob(name):
                    if match.is_file():
                        return match.resolve()
        return None

    def choose_destination(self, path):
        if is_inside(path, MAPS_DIR.resolve()):
            return path
        destination = self.free_name(path)
        if any(is_inside(path, (PROJECT_DIR / folder).resolve()) for folder in GAME_FOLDERS):
            self.copies.append((path, destination))
        else:
            self.moves.append((path, destination))
        return destination

    def free_name(self, path):
        """Where `path` goes in maps: its own name, or e.g. tiles_2.png if a
        different tiles.png is already there."""
        taken = set(self.destinations.values())
        candidate = MAPS_DIR / path.name
        if candidate.is_file() and candidate not in taken and filecmp.cmp(str(path), str(candidate), shallow=False):
            return candidate  # the same file is already there
        name = path.name
        count = 2
        while candidate.exists() or candidate in taken:
            candidate = MAPS_DIR / "{}_{}{}".format(Path(name).stem, count, Path(name).suffix)
            count += 1
        return candidate

    def new_path_text(self, owner, target):
        """How `owner`, in its new place, should refer to `target`."""
        relative = os.path.relpath(str(self.destinations[target]), str(self.destinations[owner].parent))
        return relative.replace(os.sep, "/")

    def path_fixes(self):
        return [
            (owner, element, self.new_path_text(owner, target))
            for owner, element, target in self.references
            if element.get("source") != self.new_path_text(owner, target)
        ]

    def show(self):
        if self.moves:
            print("\nThese files will be moved into the maps folder:")
            for source, destination in sorted(self.moves):
                print("  {}  ->  maps/{}".format(short(source), destination.name))
        if self.copies:
            print("\nThese are used by your game too, so they will be copied into maps, not moved:")
            for source, destination in sorted(self.copies):
                print("  {}  ->  maps/{}".format(short(source), destination.name))
        fixes = self.path_fixes()
        if fixes:
            print("\nPaths inside these files will be fixed:")
            for owner in sorted(set(owner for owner, _, _ in fixes)):
                print("  maps/{}".format(self.destinations[owner].name))
        self.show_missing()

    def show_missing(self):
        if self.missing:
            print("\nThese files couldn't be found anywhere. Put them in the maps folder, then run this again:")
            for owner, written in self.missing:
                print("  {}  (used by {})".format(written, owner.name))

    def carry_out(self):
        MAPS_DIR.mkdir(exist_ok=True)
        fixes = self.path_fixes()
        for source, destination in self.moves:
            if destination.exists():
                source.unlink()  # an identical file is already in maps
            else:
                shutil.move(str(source), str(destination))
        for source, destination in self.copies:
            if not destination.exists():
                shutil.copy2(str(source), str(destination))
        for _, element, new_text in fixes:
            element.set("source", new_text)
        for owner in set(owner for owner, _, _ in fixes):
            self.trees[owner].write(str(self.destinations[owner]), encoding="UTF-8", xml_declaration=True)
        print("\nDone.")

        reopen = sorted(
            destination.name for _, destination in self.moves + self.copies
            if destination.suffix.lower() in (".tmx", ".tsx")
        )
        if reopen:
            print(
                "\nTiled still has these at their old places, and won't find them there any "
                "more. Close them in Tiled, then open them again from the maps folder:"
            )
            for name in reopen:
                print("  maps/{}".format(name))
        self.show_missing()


if __name__ == "__main__":
    main()
