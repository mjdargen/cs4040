"""Convert WAV and MP3 files in the sounds and music folders to OGG.

Pygame can't play every kind of WAV file, and some computers can't play MP3,
but OGG works everywhere. This also renames the files with
lowercase_filenames.py first.

The original files are moved to an audio_originals folder, so that the game
loads the new OGG files. (Pygame Zero Plus loads a .wav or .mp3 before an .ogg
with the same name.)

Needs ffmpeg: https://ffmpeg.org (on macOS: brew install ffmpeg).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

from lowercase_filenames import rename_files

# The scripts in utils/ always work on the project folder above them
PROJECT_DIR = Path(__file__).resolve().parent.parent
FOLDERS = ["sounds", "music"]
ORIGINALS_DIR = PROJECT_DIR / "audio_originals"

AUDIO_EXTENSIONS = (".wav", ".mp3")


def convert_audio_files(directory):
    """Convert the WAV and MP3 files in `directory`, and move the originals."""
    for root, _, files in os.walk(str(directory)):
        for file in sorted(files):
            if not file.lower().endswith(AUDIO_EXTENSIONS):
                continue
            old_path = Path(root) / file
            ogg_path = old_path.with_suffix(".ogg")
            print("Converting: {} -> {}".format(file, ogg_path.name))

            command = [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", str(old_path),
                "-c:a", "libvorbis", "-q:a", "5",  # good quality OGG Vorbis
                str(ogg_path),
            ]
            if subprocess.run(command).returncode != 0:
                print("Couldn't convert {}; it was left as it was.".format(file))
                continue

            # Move the original out of the way, keeping its folder structure
            backup = ORIGINALS_DIR / old_path.relative_to(PROJECT_DIR)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_path), str(backup))


def main():
    if shutil.which("ffmpeg") is None:
        sys.exit(
            "This needs ffmpeg, which isn't installed (or isn't on your PATH).\n"
            "Get it from https://ffmpeg.org, or on macOS run: brew install ffmpeg"
        )

    for folder in FOLDERS:
        directory = PROJECT_DIR / folder
        if directory.exists():
            rename_files(directory)
            convert_audio_files(directory)

    print("Done converting audio.")
    if ORIGINALS_DIR.exists():
        print("The original files are in {}. Delete it once you're happy with the new ones.".format(ORIGINALS_DIR))


if __name__ == "__main__":
    main()
