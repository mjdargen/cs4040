import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk

try:
    NEAREST = Image.Resampling.NEAREST
except AttributeError:
    NEAREST = Image.NEAREST


selected_file_path = None


def parse_positive_int(text, field_name):
    text = text.strip()

    if not text:
        raise ValueError(f"{field_name} is required.")

    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"{field_name} must be a whole number.")

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")

    return value


def parse_nonnegative_int(text, field_name):
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


def get_frame_settings():
    frame_width = parse_positive_int(frame_width_var.get(), "Original frame width")
    frame_height = parse_positive_int(frame_height_var.get(), "Original frame height")
    return frame_width, frame_height


def get_crop_settings():
    mode = crop_mode_var.get()

    if mode == "center":
        return {
            "mode": "center",
            "center_width": parse_positive_int(center_width_var.get(), "New frame width"),
            "center_height": parse_positive_int(center_height_var.get(), "New frame height"),
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


def get_crop_keep_rect(frame, crop_settings):
    width, height = frame.size
    mode = crop_settings["mode"]

    if mode == "center":
        target_width = crop_settings["center_width"]
        target_height = crop_settings["center_height"]

        if target_width > width or target_height > height:
            raise ValueError(
                f"New frame size {target_width}x{target_height} is larger than "
                f"the original frame size {width}x{height}."
            )

        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        return left, top, right, bottom

    if mode == "edges":
        left = crop_settings["crop_left"]
        top = crop_settings["crop_top"]
        right = width - crop_settings["crop_right"]
        bottom = height - crop_settings["crop_bottom"]

        if left >= right:
            raise ValueError(f"Left + right crop is too large for frame width {width}.")

        if top >= bottom:
            raise ValueError(f"Top + bottom crop is too large for frame height {height}.")

        return left, top, right, bottom

    raise ValueError(f"Unknown crop mode: {mode}")


def split_sprite_sheet(image, frame_width, frame_height):
    if image.width % frame_width != 0:
        raise ValueError(f"Sheet width {image.width}px is not evenly divisible by frame width {frame_width}px.")

    if image.height % frame_height != 0:
        raise ValueError(f"Sheet height {image.height}px is not evenly divisible by frame height {frame_height}px.")

    columns = image.width // frame_width
    rows = image.height // frame_height

    frames = []

    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            frame = image.crop((x, y, x + frame_width, y + frame_height))
            frames.append(frame)

    return frames, rows, columns


def rebuild_sprite_sheet(frames, rows, columns):
    new_frame_width = frames[0].width
    new_frame_height = frames[0].height

    new_sheet = Image.new(
        "RGBA",
        (columns * new_frame_width, rows * new_frame_height),
        (0, 0, 0, 0),
    )

    for index, frame in enumerate(frames):
        row = index // columns
        col = index % columns

        x = col * new_frame_width
        y = row * new_frame_height

        new_sheet.alpha_composite(frame, (x, y))

    return new_sheet


def load_first_frame():
    if not selected_file_path:
        raise ValueError("Select a sprite sheet first.")

    frame_width, frame_height = get_frame_settings()
    image = Image.open(selected_file_path).convert("RGBA")

    return image.crop((0, 0, frame_width, frame_height))


def draw_preview():
    preview_canvas.delete("all")

    if not selected_file_path:
        preview_status_var.set("Select a sprite sheet to preview the first frame.")
        return

    try:
        frame = load_first_frame()
        crop_settings = get_crop_settings()
        keep_left, keep_top, keep_right, keep_bottom = get_crop_keep_rect(frame, crop_settings)

    except Exception as e:
        preview_status_var.set(f"Preview error: {e}")
        return

    canvas_width = int(preview_canvas["width"])
    canvas_height = int(preview_canvas["height"])

    scale = min(canvas_width / frame.width, canvas_height / frame.height)

    display_width = max(1, int(frame.width * scale))
    display_height = max(1, int(frame.height * scale))

    display_image = frame.resize((display_width, display_height), NEAREST)
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

    preview_canvas.create_rectangle(
        image_left, image_top, image_right, scaled_top, fill="gray", stipple="gray50", outline=""
    )
    preview_canvas.create_rectangle(
        image_left, scaled_bottom, image_right, image_bottom, fill="gray", stipple="gray50", outline=""
    )
    preview_canvas.create_rectangle(
        image_left, scaled_top, scaled_left, scaled_bottom, fill="gray", stipple="gray50", outline=""
    )
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

    preview_status_var.set(
        f"Original frame: {frame.width}x{frame.height}. "
        f"New frame: {cropped_width}x{cropped_height}. "
        f"Red rectangle = kept area."
    )


def select_sprite_sheet():
    global selected_file_path

    file_path = filedialog.askopenfilename(
        title="Select Sprite Sheet",
        filetypes=[
            ("PNG files", "*.png"),
            ("Image files", "*.png"),
        ],
    )

    if not file_path:
        return

    selected_file_path = file_path
    selected_file_var.set(f"Selected: {Path(file_path).name}")
    draw_preview()


def export_trimmed_sheet():
    if not selected_file_path:
        messagebox.showwarning("No file selected", "Please select a sprite sheet first.")
        return

    try:
        frame_width, frame_height = get_frame_settings()
        crop_settings = get_crop_settings()

        image = Image.open(selected_file_path).convert("RGBA")
        frames, rows, columns = split_sprite_sheet(image, frame_width, frame_height)

        cropped_frames = []

        for frame in frames:
            keep_rect = get_crop_keep_rect(frame, crop_settings)
            cropped_frames.append(frame.crop(keep_rect))

        new_sheet = rebuild_sprite_sheet(cropped_frames, rows, columns)

        original_path = Path(selected_file_path)
        default_name = original_path.with_name(original_path.stem + "_trimmed.png")

        save_path = filedialog.asksaveasfilename(
            title="Save Trimmed Sprite Sheet",
            initialfile=default_name.name,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
        )

        if not save_path:
            return

        new_sheet.save(save_path)

        messagebox.showinfo(
            "Success",
            f"Trimmed sprite sheet saved at:\n{save_path}\n\n"
            f"Old frame size: {frame_width}x{frame_height}\n"
            f"New frame size: {cropped_frames[0].width}x{cropped_frames[0].height}",
        )

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


def set_widget_state(widget, enabled=True):
    widget.configure(state="normal" if enabled else "disabled")


def update_crop_ui(*_args):
    mode = crop_mode_var.get()

    center_enabled = mode == "center"
    edge_enabled = mode == "edges"

    for widget in center_crop_widgets:
        set_widget_state(widget, center_enabled)

    for widget in edge_crop_widgets:
        set_widget_state(widget, edge_enabled)

    draw_preview()


def attach_preview_traces():
    watched_vars = [
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
        var.trace_add("write", lambda *_args: draw_preview())


root = tk.Tk()
root.title("Sprite Sheet Padding Remover")
root.geometry("760x760")
root.minsize(760, 720)

main = ttk.Frame(root, padding=12)
main.pack(fill="both", expand=True)

file_frame = ttk.LabelFrame(main, text="Sprite Sheet", padding=10)
file_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
file_frame.columnconfigure(0, weight=1)

selected_file_var = tk.StringVar(value="No sprite sheet selected yet.")

ttk.Label(file_frame, textvariable=selected_file_var, wraplength=680, justify="left").grid(
    row=0, column=0, sticky="w", pady=(0, 8)
)

ttk.Button(file_frame, text="Select Sprite Sheet", command=select_sprite_sheet).grid(row=1, column=0, sticky="w")


frame_settings = ttk.LabelFrame(main, text="Original Frame Grid", padding=10)
frame_settings.grid(row=1, column=0, sticky="ew", pady=(0, 10))
frame_settings.columnconfigure(1, weight=1)
frame_settings.columnconfigure(3, weight=1)

frame_width_var = tk.StringVar()
frame_height_var = tk.StringVar()

ttk.Label(frame_settings, text="Original frame width:").grid(row=0, column=0, sticky="w")
ttk.Entry(frame_settings, textvariable=frame_width_var, width=12).grid(row=0, column=1, sticky="w", padx=(0, 20))

ttk.Label(frame_settings, text="Original frame height:").grid(row=0, column=2, sticky="w")
ttk.Entry(frame_settings, textvariable=frame_height_var, width=12).grid(row=0, column=3, sticky="w")

ttk.Label(
    frame_settings,
    text=(
        "These are the current frame dimensions in the original sprite sheet, "
        "including any extra padding around each frame."
    ),
    wraplength=680,
    justify="left",
).grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 0))


crop_frame = ttk.LabelFrame(main, text="Padding Removal", padding=10)
crop_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
crop_frame.columnconfigure(1, weight=1)
crop_frame.columnconfigure(3, weight=1)

crop_mode_var = tk.StringVar(value="center")

center_width_var = tk.StringVar()
center_height_var = tk.StringVar()

crop_left_var = tk.StringVar()
crop_right_var = tk.StringVar()
crop_top_var = tk.StringVar()
crop_bottom_var = tk.StringVar()

ttk.Label(crop_frame, text="Crop mode:").grid(row=0, column=0, sticky="w")

ttk.Radiobutton(
    crop_frame,
    text="Specify new width / height",
    variable=crop_mode_var,
    value="center",
).grid(row=0, column=1, sticky="w")

ttk.Radiobutton(
    crop_frame,
    text="Specify left / right / top / bottom spacing",
    variable=crop_mode_var,
    value="edges",
).grid(row=0, column=2, columnspan=2, sticky="w")

ttk.Label(
    crop_frame,
    text=(
        "New width / height keeps a centered rectangle from each frame. "
        "Edge spacing removes the exact number of pixels you enter from each side."
    ),
    wraplength=680,
    justify="left",
).grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 8))

ttk.Label(crop_frame, text="New frame width:").grid(row=2, column=0, sticky="w")
center_width_entry = ttk.Entry(crop_frame, textvariable=center_width_var, width=12)
center_width_entry.grid(row=2, column=1, sticky="w", padx=(0, 20))

ttk.Label(crop_frame, text="New frame height:").grid(row=2, column=2, sticky="w")
center_height_entry = ttk.Entry(crop_frame, textvariable=center_height_var, width=12)
center_height_entry.grid(row=2, column=3, sticky="w")

ttk.Label(crop_frame, text="Remove left:").grid(row=3, column=0, sticky="w", pady=(8, 0))
crop_left_entry = ttk.Entry(crop_frame, textvariable=crop_left_var, width=12)
crop_left_entry.grid(row=3, column=1, sticky="w", padx=(0, 20), pady=(8, 0))

ttk.Label(crop_frame, text="Remove right:").grid(row=3, column=2, sticky="w", pady=(8, 0))
crop_right_entry = ttk.Entry(crop_frame, textvariable=crop_right_var, width=12)
crop_right_entry.grid(row=3, column=3, sticky="w", pady=(8, 0))

ttk.Label(crop_frame, text="Remove top:").grid(row=4, column=0, sticky="w", pady=(8, 0))
crop_top_entry = ttk.Entry(crop_frame, textvariable=crop_top_var, width=12)
crop_top_entry.grid(row=4, column=1, sticky="w", padx=(0, 20), pady=(8, 0))

ttk.Label(crop_frame, text="Remove bottom:").grid(row=4, column=2, sticky="w", pady=(8, 0))
crop_bottom_entry = ttk.Entry(crop_frame, textvariable=crop_bottom_var, width=12)
crop_bottom_entry.grid(row=4, column=3, sticky="w", pady=(8, 0))

center_crop_widgets = [center_width_entry, center_height_entry]
edge_crop_widgets = [crop_left_entry, crop_right_entry, crop_top_entry, crop_bottom_entry]


preview_frame = ttk.LabelFrame(main, text="First Frame Preview", padding=10)
preview_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))

preview_canvas = tk.Canvas(
    preview_frame,
    width=420,
    height=300,
    background="#f0f0f0",
    highlightthickness=1,
    highlightbackground="#999999",
)
preview_canvas.grid(row=0, column=0, sticky="w")

preview_status_var = tk.StringVar(value="Select a sprite sheet to preview the first frame.")
ttk.Label(preview_frame, textvariable=preview_status_var, wraplength=680, justify="left").grid(
    row=1, column=0, sticky="w", pady=(8, 0)
)


button_frame = ttk.Frame(main)
button_frame.grid(row=4, column=0, sticky="ew", pady=(8, 0))

ttk.Button(
    button_frame,
    text="Export Trimmed Sprite Sheet",
    command=export_trimmed_sheet,
).pack(pady=10)


crop_mode_var.trace_add("write", update_crop_ui)
attach_preview_traces()
update_crop_ui()

root.mainloop()
