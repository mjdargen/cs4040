import os
import subprocess

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

TARGETS = {
    "sounds": os.path.join(BASE_DIR, "..", "sounds"),
    "music": os.path.join(BASE_DIR, "..", "music"),
}


def to_snake_case(name):
    new_name = ""
    for i, letter in enumerate(name):
        if letter.isupper():
            if i != 0 and name[i - 1] not in "_ ":
                new_name += "_"
            new_name += letter.lower()
        else:
            new_name += letter

    # normalize
    new_name = new_name.replace(" ", "_")
    while "__" in new_name:
        new_name = new_name.replace("__", "_")

    return new_name.strip("_")


def process_all_files():
    remove_sounds = input("Remove original files in sounds folder? (y/n): ").lower() == "y"
    remove_music = input("Remove original files in music folder? (y/n): ").lower() == "y"

    for key, DIR_PATH in TARGETS.items():
        for root, dirs, files in os.walk(DIR_PATH):
            for file in files:
                if file.lower().endswith((".wav", ".mp3")):

                    # --- STEP 1: rename to snake_case ---
                    base, ext = os.path.splitext(file)
                    ext = ext.lower()
                    new_base = to_snake_case(base)
                    new_filename = new_base + ext

                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, new_filename)

                    if old_path != new_path:
                        os.rename(old_path, new_path)

                    # --- STEP 2: convert to .ogg ---
                    ogg_path = os.path.join(root, new_base + ".ogg")

                    subprocess.run(["ffmpeg", "-y", "-i", new_path, ogg_path])

                    # --- STEP 3: optionally delete original ---
                    if key == "sounds" and remove_sounds:
                        os.remove(new_path)
                    elif key == "music" and remove_music:
                        os.remove(new_path)


# Example Usage
if __name__ == "__main__":
    process_all_files()
    print("Done.")
