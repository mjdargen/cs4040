import os
import shutil
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
MAPS_DIR = os.path.join(PROJECT_DIR, "maps")

TMX_EXT = ".tmx"
TSX_EXT = ".tsx"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")


def ensure_maps_folder():
    os.makedirs(MAPS_DIR, exist_ok=True)


def find_files(extension, search_dirs):
    matches = []

    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue

        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.lower().endswith(extension):
                    matches.append(os.path.join(root, file))

    return matches


def find_by_basename(filename):
    matches = []

    for root, _, files in os.walk(PROJECT_DIR):
        for file in files:
            if file == filename:
                matches.append(os.path.join(root, file))

    return matches


def get_unique_path(destination_folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(destination_folder, filename)

    count = 2
    while os.path.exists(candidate):
        candidate = os.path.join(destination_folder, f"{base}_{count}{ext}")
        count += 1

    return candidate


def move_to_maps(path):
    path = os.path.abspath(path)

    if os.path.dirname(path) == os.path.abspath(MAPS_DIR):
        return path

    destination = os.path.join(MAPS_DIR, os.path.basename(path))

    if os.path.exists(destination):
        if os.path.samefile(path, destination):
            return destination

        destination = get_unique_path(MAPS_DIR, os.path.basename(path))

    print(f"Moving {path} -> {destination}")
    shutil.move(path, destination)

    return destination


def resolve_reference(source_file, referenced_path):
    if not referenced_path:
        return None

    source_folder = os.path.dirname(source_file)

    direct_path = os.path.abspath(os.path.join(source_folder, referenced_path))

    if os.path.exists(direct_path):
        return direct_path

    filename = os.path.basename(referenced_path)
    matches = find_by_basename(filename)

    if matches:
        return matches[0]

    return None


def fix_tmx_file(tmx_path):
    tree = ET.parse(tmx_path)
    root = tree.getroot()

    changed = False

    for tileset in root.findall("tileset"):
        source = tileset.get("source")

        if not source:
            continue

        tsx_path = resolve_reference(tmx_path, source)

        if tsx_path is None:
            print(f"Could not find tileset: {source}")
            continue

        new_tsx_path = move_to_maps(tsx_path)
        new_source = os.path.basename(new_tsx_path)

        if source != new_source:
            tileset.set("source", new_source)
            changed = True

        fix_tsx_file(new_tsx_path)

    if changed:
        tree.write(tmx_path, encoding="UTF-8", xml_declaration=True)
        print(f"Updated TMX references: {tmx_path}")


def fix_tsx_file(tsx_path):
    tree = ET.parse(tsx_path)
    root = tree.getroot()

    image = root.find("image")

    if image is None:
        print(f"No image tag found in: {tsx_path}")
        return

    source = image.get("source")

    if not source:
        print(f"No image source found in: {tsx_path}")
        return

    image_path = resolve_reference(tsx_path, source)

    if image_path is None:
        print(f"Could not find tilesheet image: {source}")
        return

    new_image_path = move_to_maps(image_path)
    new_source = os.path.basename(new_image_path)

    if source != new_source:
        image.set("source", new_source)
        tree.write(tsx_path, encoding="UTF-8", xml_declaration=True)
        print(f"Updated TSX image reference: {tsx_path}")


def main():
    ensure_maps_folder()

    search_dirs = [
        PROJECT_DIR,
        MAPS_DIR,
    ]

    tmx_files = find_files(TMX_EXT, search_dirs)

    for tmx_path in tmx_files:
        new_tmx_path = move_to_maps(tmx_path)
        fix_tmx_file(new_tmx_path)

    tsx_files = find_files(TSX_EXT, [MAPS_DIR])

    for tsx_path in tsx_files:
        fix_tsx_file(tsx_path)

    print("Done fixing tilemap files.")


if __name__ == "__main__":
    main()
