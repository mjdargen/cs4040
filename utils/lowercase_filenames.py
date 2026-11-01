"""Rename asset files so Pygame Zero Plus can load them by name.

Names become lowercase, with underscores between words, e.g. PlayerIdle.png
becomes player_idle.png and "tiles (1).png" becomes tiles_1.png. Then they
work as Actor("player_idle") and as images.player_idle.

This renames the files in the images, sprites, sounds, music and fonts
folders. Your code still uses the old names, so update it afterwards.
"""
import os
import re
from pathlib import Path

# The scripts in utils/ always work on the project folder above them
PROJECT_DIR = Path(__file__).resolve().parent.parent

TARGETS = [PROJECT_DIR / folder for folder in ("images", "sprites", "sounds", "music", "fonts")]

EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp",  # images
    ".wav", ".mp3", ".ogg", ".oga",  # sounds and music
    ".ttf",  # fonts
)


def clean_name(name):
    """PlayerIdle -> player_idle, HUDIcon -> hud_icon, "tiles (1)" -> tiles_1"""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)  # playerIdle -> player_Idle
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)  # HUDIcon -> HUD_Icon
    name = re.sub(r"[^a-z0-9]+", "_", name.lower())  # spaces, hyphens, brackets -> _
    return name.strip("_")


def rename_files(directory):
    """Rename the files in `directory` and its subfolders.

    Return a list of (old name, new name) for the files that were renamed.
    """
    renamed = []
    for root, _, files in os.walk(str(directory)):
        for file in sorted(files):
            base, ext = os.path.splitext(file)
            if ext.lower() not in EXTENSIONS:
                continue

            new_base = clean_name(base)
            if not new_base:
                print("Skipping {}: rename it to a name with letters in it.".format(file))
                continue
            if new_base[0].isdigit():
                print("Note: {} starts with a number, so it can't be used as images.{}. "
                      "Rename it so it starts with a letter.".format(file, new_base))

            new_file = new_base + ext.lower()
            if new_file == file:
                continue
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, new_file)
            # On Windows and macOS, a name that only differs in capitals is the
            # same file, which is fine to rename
            if os.path.exists(new_path) and not os.path.samefile(old_path, new_path):
                print("Skipping {}: {} already exists. Rename one of them yourself.".format(file, new_file))
                continue

            print("Renaming: {} -> {}".format(file, new_file))
            os.rename(old_path, new_path)
            renamed.append((base, new_base))
    return renamed


def main():
    renamed = []
    for directory in TARGETS:
        if directory.exists():
            renamed += rename_files(directory)

    if renamed:
        print("\nIf your code uses these, change it to the new names:")
        for old, new in renamed:
            print("  {} -> {}".format(old, new))
    print("Done renaming files.")


if __name__ == "__main__":
    main()
