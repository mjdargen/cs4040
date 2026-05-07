import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

TARGETS = [
    os.path.join(BASE_DIR, "..", "images"),
    os.path.join(BASE_DIR, "..", "sprites"),
    os.path.join(BASE_DIR, "..", "sounds"),
    os.path.join(BASE_DIR, "..", "music"),
]

EXTENSIONS = (".png", ".jpg", ".jpeg", ".wav", ".mp3", ".ogg")


def to_snake_case(name):
    new_name = ""

    for i, letter in enumerate(name):
        if letter.isupper():
            if i != 0 and name[i - 1] not in "_ ":
                new_name += "_"
            new_name += letter.lower()
        else:
            new_name += letter

    new_name = new_name.replace(" ", "_")

    while "__" in new_name:
        new_name = new_name.replace("__", "_")

    return new_name.strip("_")


def rename_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(EXTENSIONS):
                base, ext = os.path.splitext(file)

                old_path = os.path.join(root, file)
                new_filename = to_snake_case(base) + ext.lower()
                new_path = os.path.join(root, new_filename)

                if old_path != new_path:
                    print(f"Renaming: {file} → {new_filename}")
                    os.rename(old_path, new_path)


def main():
    for directory in TARGETS:
        if os.path.exists(directory):
            rename_files(directory)
    print("Done converting filenames.")


if __name__ == "__main__":
    main()
