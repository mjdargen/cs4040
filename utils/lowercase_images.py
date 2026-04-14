import os


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


def process_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".png"):
                base = file[:-4]  # remove .png
                new_base = to_snake_case(base)
                new_filename = new_base + ".png"

                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_filename)

                if old_path != new_path:
                    os.rename(old_path, new_path)


if __name__ == "__main__":
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "images")
    process_all_files(directory)
    print("Done.")
