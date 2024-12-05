import os
import re
import subprocess
import json


def extract_metadata(aseprite_path, file_path):
    """Extract metadata from a given Aseprite file using the Aseprite CLI."""
    try:
        # Command to extract metadata and animation tags using the Aseprite CLI
        command = [
            aseprite_path,
            "-b",  # Run in background mode (no UI)
            "--list-tags",  # List tags (animations)
            "--data",
            "temp.json",  # Export sprite metadata to a temporary JSON file
            file_path,
        ]

        # Run the subprocess command
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error processing {file_path}: {result.stderr}")
            return None

        # Read the generated JSON file to extract metadata
        if not os.path.exists("temp.json"):
            print(f"No JSON output for {file_path}.")
            return None

        with open("temp.json", "r") as json_file:
            metadata = json.load(json_file)

        # Clean up the temporary JSON file
        os.remove("temp.json")

        return metadata

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return None


def generate_documentation(metadata, output_file):
    """Generate a Markdown documentation file from metadata."""
    try:
        # Extract relevant metadata
        image_width = metadata["meta"]["size"]["w"]
        image_height = metadata["meta"]["size"]["h"]
        frame = list(metadata["frames"].keys())[0]
        frame_width = metadata["frames"][frame]["frame"]["w"]
        frame_height = metadata["frames"][frame]["frame"]["h"]
        tags = metadata["meta"].get("frameTags", [])

        number_of_animations = len(tags)
        animation_data = []
        for tag in tags:
            animation_data.append({"name": tag["name"], "num_frames": abs(tag["from"] - tag["to"]) + 1})

        # Write Markdown file
        with open(output_file, "w") as doc:
            filename = os.path.splitext(os.path.basename(output_file))[0]
            doc.write(f"# {filename}.aseprite\n")
            doc.write(f"**Image Size:** {image_width}x{image_height}\n\n")
            doc.write(f"**Frame Size:** {frame_width}x{frame_height}\n\n")
            doc.write(f"**Number of Animations:** {number_of_animations}\n\n")
            doc.write("**Animations:**\n")
            for i, anim in enumerate(animation_data):
                doc.write(f"- {anim['name']} - row {i} - {anim['num_frames']} frames\n")

            doc.write("\n**Code Example:**\n```python\n")
            doc.write("# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)\n")
            doc.write("# Note: FPS set to 5 in examples below, adjust as needed)\n")
            doc.write(f'filename = "{filename}.png"\n')
            doc.write(f"frame_width = {frame_width}\n")
            doc.write(f"frame_height = {frame_height}\n")
            sprite_name = filename.lower()
            first = None
            for i, anim in enumerate(animation_data):
                anim_name = camel_to_snake(anim["name"])
                if i == 0:
                    first = f"{sprite_name}_{anim_name}"
                doc.write(f"{sprite_name}_{anim_name} = Sprite(filename, frame_width, frame_height, {i}, {anim['num_frames']}, 5)\n")
            doc.write("\n# Define SpriteActor\n")
            doc.write(f"{sprite_name} = SpriteActor({first})\n")
            doc.write("```\n")

        print(f"Documentation written to {output_file}")
    except Exception as e:
        print(f"Failed to write documentation for {output_file}: {e}")


def generate_readme(directory):
    """Generate a README.md file with an overview and links to all sprite documentation."""
    try:
        # Find all Markdown files in the directory (excluding README.md)
        markdown_files = [f for f in os.listdir(directory) if f.endswith(".md") and f != "README.md"]

        # Write the main README.md file
        with open(os.path.join(directory, "README.md"), "w") as readme:
            readme.write("# Sprite Documentation\n\n")
            readme.write(
                "This folder contains some example sprites that you can use for your projects. The `.png` files are the spritesheets you will use in your project. The `.md` files (also linked below) provide dimensions and information about each of the animations in the sprite. The `.aseprite` files are the source files used to create the sprites.\n\n"
                "Read the `.md` files first by clicking the links for the sprite you want below. Each file provides metadata about the sprite, a breakdown of animations, and example usage code.\n\n"
            )
            readme.write("## Sprite Documentation Files\n\n")

            if markdown_files:
                for md_file in sorted(markdown_files):  # Sort for consistency
                    sprite_name = os.path.splitext(md_file)[0]
                    readme.write(f"- [{sprite_name}]({md_file})\n")
            else:
                readme.write("No sprite documentation files have been generated yet.\n")

        print("README.md generated successfully.")
    except Exception as e:
        print(f"An error occurred while generating README.md: {e}")


def process_all_files(directory, aseprite_path="Aseprite"):
    """Process all Aseprite files in the given directory."""
    try:
        # Find all .aseprite files in the directory
        aseprite_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".aseprite")]

        if not aseprite_files:
            print("No .aseprite files found in the directory.")
            return

        for file_path in aseprite_files:
            print(f"Processing {file_path}...")

            # Extract metadata
            metadata = extract_metadata(aseprite_path, file_path)
            if metadata is None:
                continue

            # Generate documentation
            output_file = os.path.splitext(file_path)[0] + ".md"
            generate_documentation(metadata, output_file)

        # Generate the main README.md file
        generate_readme(directory)

    except Exception as e:
        print(f"An error occurred while processing files: {e}")


def camel_to_snake(camel_str):
    # Add an underscore before each uppercase letter, except at the start, and convert to lowercase
    snake_str = re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()
    return snake_str


# Example Usage
if __name__ == "__main__":
    directory = os.path.dirname(os.path.realpath(__file__))  # Current script directory
    process_all_files(directory)
