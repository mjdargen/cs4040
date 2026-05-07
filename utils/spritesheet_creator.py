import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageSequence, ImageTk
import re

try:
    NEAREST = Image.Resampling.NEAREST
except AttributeError:
    NEAREST = Image.NEAREST


selected_file_paths = []


def safe_variable_name(name):
    """Convert a filename or animation name into a safe Python variable name."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")

    if not name:
        name = "sprite"

    if name[0].isdigit():
        name = "_" + name

    return name


def parse_optional_positive_int(text, field_name):
    """Return None for blank input, otherwise a positive integer."""
    text = text.strip()

    if not text:
        return None

    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"{field_name} must be a whole number.")

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")

    return value


def parse_nonnegative_int(text, field_name):
    """Return 0 for blank input, otherwise a nonnegative integer."""
    text = text.strip()

    if not text:
        return 0

    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"{field_name} must be a whole number.")

    if value < 0:
        raise ValueError(f"{field_name} must be 0 or greater.")

    return value


def get_png_frame_settings():
    """Read the PNG strip layout settings from the UI."""
    arrangement = arrangement_var.get()
    frame_width = parse_optional_positive_int(frame_width_var.get(), "Frame width")
    frame_height = parse_optional_positive_int(frame_height_var.get(), "Frame height")

    return arrangement, frame_width, frame_height


def get_crop_settings():
    """Read crop settings from the UI."""
    mode = crop_mode_var.get()

    if mode == "none":
        return {"mode": "none"}

    if mode == "center":
        center_width = parse_optional_positive_int(center_width_var.get(), "Center crop width")
        center_height = parse_optional_positive_int(center_height_var.get(), "Center crop height")

        return {
            "mode": "center",
            "center_width": center_width,
            "center_height": center_height,
        }

    if mode == "edges":
        return {
            "mode": "edges",
            "crop_left": parse_nonnegative_int(crop_left_var.get(), "Crop left"),
            "crop_right": parse_nonnegative_int(crop_right_var.get(), "Crop right"),
            "crop_top": parse_nonnegative_int(crop_top_var.get(), "Crop top"),
            "crop_bottom": parse_nonnegative_int(crop_bottom_var.get(), "Crop bottom"),
        }

    raise ValueError(f"Unknown crop mode: {mode}")


def get_crop_keep_rect(image, crop_settings):
    """
    Return the rectangle that should be kept after cropping.

    The result is a Pillow crop box:
    (left, top, right, bottom)
    """
    width, height = image.size
    mode = crop_settings["mode"]

    if mode == "none":
        return 0, 0, width, height

    if mode == "center":
        target_width = crop_settings["center_width"]
        target_height = crop_settings["center_height"]

        if target_width is None or target_height is None:
            raise ValueError("Center crop needs both a width and a height.")

        if target_width > width or target_height > height:
            raise ValueError(
                f"Center crop size {target_width}x{target_height} is larger than " f"the frame size {width}x{height}."
            )

        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        return left, top, right, bottom

    if mode == "edges":
        left = crop_settings["crop_left"]
        right_crop = crop_settings["crop_right"]
        top = crop_settings["crop_top"]
        bottom_crop = crop_settings["crop_bottom"]

        right = width - right_crop
        bottom = height - bottom_crop

        if left >= right:
            raise ValueError(f"Left + right crop is too large for frame width {width}.")

        if top >= bottom:
            raise ValueError(f"Top + bottom crop is too large for frame height {height}.")

        return left, top, right, bottom

    raise ValueError(f"Unknown crop mode: {mode}")


def apply_frame_crop(image, crop_settings):
    """Crop one frame using the chosen crop settings."""
    keep_rect = get_crop_keep_rect(image, crop_settings)
    return image.crop(keep_rect)


def gif_to_frames(gif_path, crop_settings):
    """Load all frames from a GIF as RGBA images and crop each frame."""
    frames = []

    with Image.open(gif_path) as gif:
        for frame in ImageSequence.Iterator(gif):
            frame_image = frame.convert("RGBA").copy()
            frame_image = apply_frame_crop(frame_image, crop_settings)
            frames.append(frame_image)

    return frames


def png_to_frames(png_path, arrangement, frame_width, frame_height, crop_settings):
    """
    Load a PNG sprite strip and split it into frames.

    For rows:
        Frames run left to right.
        Default frame height = full image height.
        Default frame width = frame height.

    For columns:
        Frames run top to bottom.
        Default frame width = full image width.
        Default frame height = frame width.
    """
    image = Image.open(png_path).convert("RGBA")

    if arrangement == "rows":
        resolved_frame_height = frame_height if frame_height is not None else image.height
        resolved_frame_width = frame_width if frame_width is not None else resolved_frame_height

        if resolved_frame_height != image.height:
            raise ValueError(
                f"{png_path.name}: for row strips, this script expects the full PNG height "
                f"to be one frame tall. The image is {image.height}px tall, but frame height "
                f"was set to {resolved_frame_height}px."
            )

        if image.width % resolved_frame_width != 0:
            raise ValueError(
                f"{png_path.name}: image width {image.width}px is not evenly divisible by "
                f"frame width {resolved_frame_width}px."
            )

        frames = []

        for x in range(0, image.width, resolved_frame_width):
            frame = image.crop((x, 0, x + resolved_frame_width, resolved_frame_height))
            frame = apply_frame_crop(frame, crop_settings)
            frames.append(frame)

        return frames

    if arrangement == "columns":
        resolved_frame_width = frame_width if frame_width is not None else image.width
        resolved_frame_height = frame_height if frame_height is not None else resolved_frame_width

        if resolved_frame_width != image.width:
            raise ValueError(
                f"{png_path.name}: for column strips, this script expects the full PNG width "
                f"to be one frame wide. The image is {image.width}px wide, but frame width "
                f"was set to {resolved_frame_width}px."
            )

        if image.height % resolved_frame_height != 0:
            raise ValueError(
                f"{png_path.name}: image height {image.height}px is not evenly divisible by "
                f"frame height {resolved_frame_height}px."
            )

        frames = []

        for y in range(0, image.height, resolved_frame_height):
            frame = image.crop((0, y, resolved_frame_width, y + resolved_frame_height))
            frame = apply_frame_crop(frame, crop_settings)
            frames.append(frame)

        return frames

    raise ValueError(f"Unsupported PNG arrangement: {arrangement}")


def load_animation_frames(file_path, arrangement, frame_width, frame_height, crop_settings):
    """Load frames from either a GIF or a PNG sprite strip."""
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".gif":
        frames = gif_to_frames(path, crop_settings)

    elif extension == ".png":
        frames = png_to_frames(
            path,
            arrangement=arrangement,
            frame_width=frame_width,
            frame_height=frame_height,
            crop_settings=crop_settings,
        )

    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    if not frames:
        raise ValueError(f"No frames found in {path.name}")

    return {
        "name": path.stem,
        "frames": frames,
        "frame_count": len(frames),
    }


def load_first_uncropped_frame(file_path):
    """
    Load the first frame from the first selected file before crop is applied.

    This is used only for the preview.
    """
    arrangement, frame_width, frame_height = get_png_frame_settings()

    no_crop = {"mode": "none"}
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".gif":
        with Image.open(path) as gif:
            first_frame = next(ImageSequence.Iterator(gif))
            return first_frame.convert("RGBA").copy()

    if extension == ".png":
        frames = png_to_frames(
            path,
            arrangement=arrangement,
            frame_width=frame_width,
            frame_height=frame_height,
            crop_settings=no_crop,
        )
        return frames[0]

    raise ValueError(f"Unsupported file type: {path.suffix}")


def pad_to_canvas(image, canvas_width, canvas_height):
    """Center an image on a transparent canvas of a fixed size."""
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))

    x = (canvas_width - image.width) // 2
    y = (canvas_height - image.height) // 2

    canvas.alpha_composite(image, (x, y))
    return canvas


def generate_markdown(save_path, sheet_width, sheet_height, frame_width, frame_height, animations, fps):
    """Generate a Markdown documentation file for the sprite sheet."""
    save_path = Path(save_path)
    sheet_filename = save_path.name
    sheet_stem = safe_variable_name(save_path.stem)

    lines = []

    lines.append(f"# {sheet_filename}")
    lines.append("")
    lines.append(f"**Image Size:** {sheet_width}x{sheet_height}")
    lines.append("")
    lines.append(f"**Frame Size:** {frame_width}x{frame_height}")
    lines.append("")
    lines.append(f"**Number of Animations:** {len(animations)}")
    lines.append("")
    lines.append("**Animations:**")

    for row, anim in enumerate(animations):
        lines.append(f"- {anim['name']} - row {row} - {anim['frame_count']} frames")

    lines.append("")
    lines.append("**Code Example:**")
    lines.append("```python")
    lines.append("# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)")
    lines.append(f"# Note: FPS set to {fps} in examples below, adjust as needed)")
    lines.append(f'filename = "{sheet_filename}"')
    lines.append(f"frame_width = {frame_width}")
    lines.append(f"frame_height = {frame_height}")

    for row, anim in enumerate(animations):
        anim_name = safe_variable_name(anim["name"])
        frame_count = anim["frame_count"]

        lines.append(
            f"{sheet_stem}_{anim_name} = Sprite(filename, frame_width, frame_height, {row}, {frame_count}, {fps})"
        )

    first_anim_name = safe_variable_name(animations[0]["name"])

    lines.append("")
    lines.append("# Define SpriteActor")
    lines.append(f"{sheet_stem} = SpriteActor({sheet_stem}_{first_anim_name})")
    lines.append("```")
    lines.append("")

    markdown_path = save_path.with_suffix(".md")
    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    return markdown_path


def draw_crop_preview():
    """Redraw the preview image and crop overlay."""
    preview_canvas.delete("all")

    if not selected_file_paths:
        preview_status_var.set("Select images to preview the first frame.")
        return

    try:
        raw_frame = load_first_uncropped_frame(selected_file_paths[0])
        crop_settings = get_crop_settings()
        keep_left, keep_top, keep_right, keep_bottom = get_crop_keep_rect(raw_frame, crop_settings)

    except Exception as e:
        preview_status_var.set(f"Preview error: {e}")
        return

    canvas_width = int(preview_canvas["width"])
    canvas_height = int(preview_canvas["height"])

    image_width, image_height = raw_frame.size

    scale = min(
        canvas_width / image_width,
        canvas_height / image_height,
        1 if image_width <= canvas_width and image_height <= canvas_height else 999,
    )

    display_width = max(1, int(image_width * scale))
    display_height = max(1, int(image_height * scale))

    display_image = raw_frame.resize((display_width, display_height), NEAREST)
    photo = ImageTk.PhotoImage(display_image)

    preview_canvas.preview_photo = photo

    offset_x = (canvas_width - display_width) // 2
    offset_y = (canvas_height - display_height) // 2

    preview_canvas.create_image(offset_x, offset_y, anchor="nw", image=photo)

    scaled_left = offset_x + keep_left * scale
    scaled_top = offset_y + keep_top * scale
    scaled_right = offset_x + keep_right * scale
    scaled_bottom = offset_y + keep_bottom * scale

    image_left = offset_x
    image_top = offset_y
    image_right = offset_x + display_width
    image_bottom = offset_y + display_height

    crop_mode = crop_mode_var.get()

    if crop_mode != "none":
        # Top cropped area
        preview_canvas.create_rectangle(
            image_left, image_top, image_right, scaled_top, fill="gray", stipple="gray50", outline=""
        )

        # Bottom cropped area
        preview_canvas.create_rectangle(
            image_left, scaled_bottom, image_right, image_bottom, fill="gray", stipple="gray50", outline=""
        )

        # Left cropped area
        preview_canvas.create_rectangle(
            image_left, scaled_top, scaled_left, scaled_bottom, fill="gray", stipple="gray50", outline=""
        )

        # Right cropped area
        preview_canvas.create_rectangle(
            scaled_right, scaled_top, image_right, scaled_bottom, fill="gray", stipple="gray50", outline=""
        )

    preview_canvas.create_rectangle(
        scaled_left,
        scaled_top,
        scaled_right,
        scaled_bottom,
        outline="red",
        width=2,
    )

    cropped_width = keep_right - keep_left
    cropped_height = keep_bottom - keep_top

    preview_name = Path(selected_file_paths[0]).name
    preview_status_var.set(
        f"Previewing {preview_name}: original frame {image_width}x{image_height}, "
        f"cropped frame {cropped_width}x{cropped_height}. Red rectangle = kept area."
    )


def select_images():
    """Select PNG or GIF files, then update the preview."""
    global selected_file_paths

    file_paths = filedialog.askopenfilenames(
        title="Select PNG or GIF files",
        filetypes=[
            ("Image files", "*.png *.gif"),
            ("PNG files", "*.png"),
            ("GIF files", "*.gif"),
        ],
    )

    if not file_paths:
        return

    selected_file_paths = list(file_paths)

    if len(selected_file_paths) == 1:
        selected_files_var.set(f"Selected 1 file: {Path(selected_file_paths[0]).name}")
    else:
        selected_files_var.set(f"Selected {len(selected_file_paths)} files. Previewing first file.")

    draw_crop_preview()


def build_sprite_sheet():
    """Build the sprite sheet and Markdown file from the selected images."""
    if not selected_file_paths:
        messagebox.showwarning("No files selected", "Please select PNG or GIF files first.")
        return

    try:
        arrangement, frame_width, frame_height = get_png_frame_settings()
        crop_settings = get_crop_settings()

        fps = 5

        animations = []

        for file_path in selected_file_paths:
            animation = load_animation_frames(
                file_path,
                arrangement=arrangement,
                frame_width=frame_width,
                frame_height=frame_height,
                crop_settings=crop_settings,
            )
            animations.append(animation)

        final_frame_width = max(frame.width for anim in animations for frame in anim["frames"])
        final_frame_height = max(frame.height for anim in animations for frame in anim["frames"])

        max_frames = max(anim["frame_count"] for anim in animations)

        sheet_width = max_frames * final_frame_width
        sheet_height = len(animations) * final_frame_height

        spritesheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))

        for row, anim in enumerate(animations):
            y = row * final_frame_height

            for col, frame in enumerate(anim["frames"]):
                x = col * final_frame_width
                padded_frame = pad_to_canvas(frame, final_frame_width, final_frame_height)
                spritesheet.alpha_composite(padded_frame, (x, y))

        save_path = filedialog.asksaveasfilename(
            title="Save Sprite Sheet",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
        )

        if not save_path:
            return

        spritesheet.save(save_path)

        markdown_path = generate_markdown(
            save_path=save_path,
            sheet_width=sheet_width,
            sheet_height=sheet_height,
            frame_width=final_frame_width,
            frame_height=final_frame_height,
            animations=animations,
            fps=fps,
        )

        messagebox.showinfo(
            "Success",
            f"Sprite sheet saved at:\n{save_path}\n\nMarkdown saved at:\n{markdown_path}",
        )

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


def set_widget_state(widget, enabled=True):
    """Enable or disable a Tkinter widget."""
    widget.configure(state="normal" if enabled else "disabled")


def update_crop_ui(*_args):
    """Enable only the crop controls relevant to the selected crop mode."""
    mode = crop_mode_var.get()

    center_enabled = mode == "center"
    edges_enabled = mode == "edges"

    for widget in center_crop_widgets:
        set_widget_state(widget, center_enabled)

    for widget in edge_crop_widgets:
        set_widget_state(widget, edges_enabled)

    draw_crop_preview()


def attach_preview_traces():
    """Redraw preview whenever a relevant setting changes."""
    watched_vars = [
        arrangement_var,
        frame_width_var,
        frame_height_var,
        crop_mode_var,
        center_width_var,
        center_height_var,
        crop_left_var,
        crop_right_var,
        crop_top_var,
        crop_bottom_var,
    ]

    for var in watched_vars:
        var.trace_add("write", lambda *_args: draw_crop_preview())


root = tk.Tk()
root.title("PNG/GIF Sprite Sheet Combiner")
root.geometry("760x940")
root.minsize(760, 900)

main = ttk.Frame(root, padding=12)
main.pack(fill="both", expand=True)

# File selection section
file_frame = ttk.LabelFrame(main, text="Selected Images", padding=10)
file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
file_frame.columnconfigure(0, weight=1)

selected_files_var = tk.StringVar(value="No files selected yet.")

ttk.Label(file_frame, textvariable=selected_files_var, wraplength=650, justify="left").grid(
    row=0, column=0, sticky="w", pady=(0, 8)
)

ttk.Button(file_frame, text="Select PNGs / GIFs", command=select_images).grid(row=1, column=0, sticky="w")


# PNG settings section
png_frame = ttk.LabelFrame(main, text="PNG Frame Settings", padding=10)
png_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
png_frame.columnconfigure(1, weight=1)
png_frame.columnconfigure(3, weight=1)

arrangement_var = tk.StringVar(value="rows")
frame_width_var = tk.StringVar()
frame_height_var = tk.StringVar()

ttk.Label(png_frame, text="Input arrangement:").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(png_frame, text="Rows", variable=arrangement_var, value="rows").grid(row=0, column=1, sticky="w")
ttk.Radiobutton(png_frame, text="Columns", variable=arrangement_var, value="columns").grid(row=0, column=2, sticky="w")

arrangement_desc = "For PNG strips only. Rows means frames run left to right. Columns means frames run top to bottom. "
ttk.Label(png_frame, text=arrangement_desc, wraplength=680, justify="left").grid(
    row=1, column=0, columnspan=4, sticky="w", pady=(2, 8)
)

ttk.Label(png_frame, text="Frame width, optional:").grid(row=2, column=0, sticky="w")
ttk.Entry(png_frame, textvariable=frame_width_var, width=12).grid(row=2, column=1, sticky="w", padx=(0, 20))

ttk.Label(png_frame, text="Frame height, optional:").grid(row=2, column=2, sticky="w")
ttk.Entry(png_frame, textvariable=frame_height_var, width=12).grid(row=2, column=3, sticky="w")

# frame_desc = (
#     "Leave blank to auto-detect. For row strips, the full image height is assumed to be one frame height, "
#     "and the frame width defaults to the same value. Fill these in when your frames are not square."
# )
# ttk.Label(png_frame, text=frame_desc, wraplength=680, justify="left").grid(
#     row=3, column=0, columnspan=4, sticky="w", pady=(2, 0)
# )


# Crop section
crop_frame = ttk.LabelFrame(main, text="Per-Frame Crop Settings", padding=10)
crop_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
crop_frame.columnconfigure(1, weight=1)
crop_frame.columnconfigure(3, weight=1)

crop_mode_var = tk.StringVar(value="none")
center_width_var = tk.StringVar()
center_height_var = tk.StringVar()
crop_left_var = tk.StringVar()
crop_right_var = tk.StringVar()
crop_top_var = tk.StringVar()
crop_bottom_var = tk.StringVar()

ttk.Label(crop_frame, text="Crop mode:").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(crop_frame, text="None", variable=crop_mode_var, value="none").grid(row=0, column=1, sticky="w")
ttk.Radiobutton(crop_frame, text="Center size", variable=crop_mode_var, value="center").grid(
    row=0, column=2, sticky="w"
)
ttk.Radiobutton(crop_frame, text="Edge crop", variable=crop_mode_var, value="edges").grid(row=0, column=3, sticky="w")

crop_desc = (
    "Crop is applied to each extracted frame. Center size keeps a centered rectangle of the size you enter. "
    "Edge crop removes specific pixels from each side."
)
ttk.Label(crop_frame, text=crop_desc, wraplength=680, justify="left").grid(
    row=1, column=0, columnspan=4, sticky="w", pady=(2, 8)
)

ttk.Label(crop_frame, text="Center crop width:").grid(row=2, column=0, sticky="w")
center_width_entry = ttk.Entry(crop_frame, textvariable=center_width_var, width=12)
center_width_entry.grid(row=2, column=1, sticky="w", padx=(0, 20))

ttk.Label(crop_frame, text="Center crop height:").grid(row=2, column=2, sticky="w")
center_height_entry = ttk.Entry(crop_frame, textvariable=center_height_var, width=12)
center_height_entry.grid(row=2, column=3, sticky="w")

ttk.Label(crop_frame, text="Crop left:").grid(row=3, column=0, sticky="w", pady=(8, 0))
crop_left_entry = ttk.Entry(crop_frame, textvariable=crop_left_var, width=12)
crop_left_entry.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=(8, 0))

ttk.Label(crop_frame, text="Crop right:").grid(row=3, column=2, sticky="w", pady=(8, 0))
crop_right_entry = ttk.Entry(crop_frame, textvariable=crop_right_var, width=12)
crop_right_entry.grid(row=3, column=3, sticky="w", pady=(8, 0))

ttk.Label(crop_frame, text="Crop top:").grid(row=4, column=0, sticky="w", pady=(8, 0))
crop_top_entry = ttk.Entry(crop_frame, textvariable=crop_top_var, width=12)
crop_top_entry.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=(8, 0))

ttk.Label(crop_frame, text="Crop bottom:").grid(row=4, column=2, sticky="w", pady=(8, 0))
crop_bottom_entry = ttk.Entry(crop_frame, textvariable=crop_bottom_var, width=12)
crop_bottom_entry.grid(row=4, column=3, sticky="w", pady=(8, 0))

center_crop_widgets = [center_width_entry, center_height_entry]
edge_crop_widgets = [crop_left_entry, crop_right_entry, crop_top_entry, crop_bottom_entry]


# Preview section
preview_frame = ttk.LabelFrame(main, text="Crop Preview", padding=10)
preview_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))

preview_canvas = tk.Canvas(
    preview_frame,
    width=420,
    height=300,
    background="#f0f0f0",
    highlightthickness=1,
    highlightbackground="#999999",
)
preview_canvas.grid(row=0, column=0, sticky="w")

preview_status_var = tk.StringVar(value="Select images to preview the first frame.")
ttk.Label(preview_frame, textvariable=preview_status_var, wraplength=680, justify="left").grid(
    row=1, column=0, sticky="w", pady=(8, 0)
)


# Build button section
button_frame = ttk.Frame(main)
button_frame.grid(row=6, column=0, sticky="ew", pady=(8, 0))

ttk.Button(
    button_frame,
    text="Build Sprite Sheet and Markdown",
    command=build_sprite_sheet,
).pack(pady=10)


crop_mode_var.trace_add("write", update_crop_ui)
attach_preview_traces()
update_crop_ui()

root.mainloop()
