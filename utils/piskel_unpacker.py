import os
import re
import json
import base64
import io
from pathlib import Path
from PIL import Image


def decode_base64_png(data_url: str) -> Image.Image:
    prefix = "data:image/png;base64,"
    if not data_url.startswith(prefix):
        raise ValueError("Expected a base64 PNG data URL.")
    raw = base64.b64decode(data_url[len(prefix) :])
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def parse_layer(layer_str: str) -> dict:
    return json.loads(layer_str)


def normalize_name(stem: str) -> str:
    """
    Convert filename to pygame-zero-friendly style:
    - lowercase
    - underscores only
    - strip common trailing date codes
    """
    name = stem.lower().strip()

    # Remove common trailing date patterns like:
    # foo_20260330
    # foo-2026-03-30
    # foo_2026_03_30
    # foo-20260330-153000
    name = re.sub(r"[-_ ]?\d{4}[-_ ]?\d{2}[-_ ]?\d{2}(?:[-_ ]?\d{2,6})?$", "", name)
    name = re.sub(r"[-_ ]?\d{8}(?:[-_ ]?\d{6})?$", "", name)

    # Replace any non-alphanumeric sequence with underscore
    name = re.sub(r"[^a-z0-9]+", "_", name)

    # Collapse repeated underscores
    name = re.sub(r"_+", "_", name).strip("_")

    if not name:
        name = "sprite"

    return name


def extract_chunk_frames(chunk: dict, fw: int, fh: int) -> dict:
    """
    Extract frames from a Piskel chunk.

    Important:
    In Piskel chunk layout, the outer list behaves like columns (x),
    and the inner lists behave like rows (y).

    So layout like [[0],[1],[2],[3]] means:
    frame 0 at column 0, row 0
    frame 1 at column 1, row 0
    frame 2 at column 2, row 0
    ...
    """
    sheet = decode_base64_png(chunk["base64PNG"])
    layout = chunk["layout"]

    frames = {}

    for col_i, column in enumerate(layout):
        for row_i, frame_index in enumerate(column):
            left = col_i * fw
            top = row_i * fh
            right = left + fw
            bottom = top + fh

            if right > sheet.width or bottom > sheet.height:
                continue

            frames[frame_index] = sheet.crop((left, top, right, bottom))

    return frames


def build_layer_frames(layer: dict, fw: int, fh: int) -> list[Image.Image]:
    count = layer["frameCount"]
    frames = [Image.new("RGBA", (fw, fh), (0, 0, 0, 0)) for _ in range(count)]

    for chunk in layer.get("chunks", []):
        chunk_frames = extract_chunk_frames(chunk, fw, fh)
        for i, img in chunk_frames.items():
            if 0 <= i < count:
                frames[i] = img

    return frames


def composite_frames(data: dict):
    p = data["piskel"]
    fw, fh = p["width"], p["height"]
    fps = p.get("fps", 12)

    hidden = set(p.get("hiddenFrames", []))

    layers = [parse_layer(layer_str) for layer_str in p["layers"]]
    layers = [layer for layer in layers if layer.get("opacity", 1) > 0]

    if not layers:
        return [], fps

    total = max(layer["frameCount"] for layer in layers)
    layer_frames = [build_layer_frames(layer, fw, fh) for layer in layers]

    final = []

    for i in range(total):
        if i in hidden:
            continue

        canvas = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))

        for layer, frames in zip(layers, layer_frames):
            if i >= len(frames):
                continue

            img = frames[i]
            opacity = layer.get("opacity", 1)

            if opacity < 1:
                img = img.copy()
                alpha = img.getchannel("A")
                alpha = alpha.point(lambda a: int(a * opacity))
                img.putalpha(alpha)

            canvas.alpha_composite(img)

        final.append(canvas)

    return final, fps


def save_frames(frames: list[Image.Image], output_dir: Path, base_name: str):
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, frame in enumerate(frames):
        frame_path = output_dir / f"{base_name}_{i:02d}.png"
        frame.save(frame_path)


def save_gif(frames: list[Image.Image], fps: int, gif_path: Path):
    if not frames:
        raise ValueError("No frames to save.")

    duration = int(1000 / fps)

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
    )


def convert_one(piskel_path: Path, output_dir: Path):
    with open(piskel_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    frames, fps = composite_frames(data)

    if not frames:
        print(f"Skipping {piskel_path.name} (no frames)")
        return

    base_name = normalize_name(piskel_path.stem)

    save_frames(frames, output_dir, base_name)
    save_gif(frames, fps, output_dir / f"{base_name}.gif")

    print(f"{piskel_path.name} -> {base_name}_##.png, {base_name}.gif")


def batch_convert(input_dir: str, output_dir: str):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        raise ValueError(f"Input folder does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.piskel"))

    if not files:
        print("No .piskel files found")
        return

    for file in files:
        try:
            convert_one(file, output_dir)
        except Exception as e:
            print(f"Failed: {file.name} -> {e}")


if __name__ == "__main__":
    INPUT_FOLDER = "utils/input_piskels"
    OUTPUT_FOLDER = "utils/output_assets"

    batch_convert(INPUT_FOLDER, OUTPUT_FOLDER)
