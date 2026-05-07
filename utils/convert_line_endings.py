from pathlib import Path

root = Path(".")

TEXT_EXTENSIONS = {
    ".py",
    ".json",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".cfg",
    ".ini",
    ".csv",
    ".tsv",
    ".sh",
    ".bash",
    ".tmx",
    ".tsx",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}


for path in root.rglob("*"):
    if any(part in SKIP_DIRS for part in path.parts):
        continue

    if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
        try:
            original = path.read_text(encoding="utf-8")
            converted = original.replace("\r\n", "\n").replace("\r", "\n")

            if converted != original:
                path.write_text(converted, encoding="utf-8", newline="\n")
                print(f"Converted: {path}")

        except UnicodeDecodeError:
            print(f"Skipped non-UTF-8 file: {path}")
        except Exception as error:
            print(f"Skipped {path}: {error}")
