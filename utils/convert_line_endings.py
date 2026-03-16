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
}

for path in root.rglob("*"):
    if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
        try:
            text = path.read_text(encoding="utf-8")
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"Converted: {path}")
        except Exception:
            pass
