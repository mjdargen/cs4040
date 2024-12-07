import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


def select_and_combine():
    # Open file dialog to select multiple PNG files
    file_paths = filedialog.askopenfilenames(
        title="Select PNG files for rows of the sprite sheet",
        filetypes=[("PNG files", "*.png")],
    )

    if not file_paths:
        messagebox.showwarning("No files selected", "Please select at least one PNG file.")
        return

    try:
        # Load images and calculate the final sprite sheet dimensions
        images = [Image.open(file) for file in file_paths]
        max_width = max(image.width for image in images)
        total_height = sum(image.height for image in images)

        # Create the blank sprite sheet
        spritesheet = Image.new("RGBA", (max_width, total_height))

        # Paste each row onto the sprite sheet
        y_offset = 0
        for image in images:
            spritesheet.paste(image, (0, y_offset))
            y_offset += image.height

        # Save the final sprite sheet
        save_path = filedialog.asksaveasfilename(
            title="Save Sprite Sheet",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
        )
        if save_path:
            spritesheet.save(save_path)
            messagebox.showinfo("Success", f"Sprite sheet saved at {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the Tkinter application
root = tk.Tk()
root.title("Sprite Sheet Combiner")
root.geometry("300x150")

# Add a button to trigger the sprite sheet creation
combine_button = tk.Button(root, text="Combine Sprite Sheet", command=select_and_combine)
combine_button.pack(expand=True, pady=20)

# Run the application
root.mainloop()
