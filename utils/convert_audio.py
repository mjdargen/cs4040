import os
import subprocess
from lowercase_filenames import rename_files

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

TARGETS = {
    "sounds": os.path.join(BASE_DIR, "..", "sounds"),
    "music": os.path.join(BASE_DIR, "..", "music"),
}

AUDIO_EXTENSIONS = (".wav", ".mp3")


def convert_audio_files(directory, remove_original=False):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(AUDIO_EXTENSIONS):
                old_path = os.path.join(root, file)
                base, _ = os.path.splitext(old_path)
                ogg_path = base + ".ogg"

                print(f"Converting: {file} → {os.path.basename(ogg_path)}")

                subprocess.run(
                    ["ffmpeg", "-y", "-i", old_path, ogg_path],
                    check=True,
                )

                if remove_original:
                    os.remove(old_path)


def main():
    remove_sounds = input("Remove original files in sounds folder? (y/n): ").lower() == "y"
    remove_music = input("Remove original files in music folder? (y/n): ").lower() == "y"

    if os.path.exists(TARGETS["sounds"]):
        rename_files(TARGETS["sounds"])
        convert_audio_files(TARGETS["sounds"], remove_sounds)

    if os.path.exists(TARGETS["music"]):
        rename_files(TARGETS["music"])
        convert_audio_files(TARGETS["music"], remove_music)

    print("Done converting audio.")


if __name__ == "__main__":
    main()
