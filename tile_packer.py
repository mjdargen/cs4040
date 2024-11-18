# requires Python Image Library or Pillow: https://pypi.org/project/Pillow/
# most run command to install: "pip install Pillow"
import os
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename

prompt = """
Before you continue, you will need the following information about your spritesheet:
    - What is the width and height of the tiles, including margins?
    - What is the width and height of the art in the tile, excluding margins?
    - What are the margins on each side of the art?
"""


def main():
    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw()
    # select file and store filename
    filename = askopenfilename(
        initialdir=os.path.dirname(os.path.realpath(__file__)),
        multiple=False,
        filetypes=(("PNG or JPG files", "*.png;*.jpg"),),
        title="Select your tileset or spritesheet image:",
    )
    # filename = "wind.png"
    
    # load old sheet
    old_sheet = Image.open(filename)
    old_pixels = old_sheet.load()

    # input
    current, future, tile_margin = get_all_data(old_sheet.width, old_sheet.height)
    tile_width, tile_height = future
    current_tile_width, current_tile_height = current

    # hardcoded
    # tile_width = 128
    # tile_height = 128
    # l r t b
    # tile_margin = [80, 80, 0, 0]
    # current_tile_width = tile_width + tile_margin[0] + tile_margin[1]
    # current_tile_height = tile_height + tile_margin[2] + tile_margin[3]

    # create new sheet
    new_sheet = Image.new(
        "RGBA",
        (
            int(old_sheet.width / current_tile_width * tile_width),
            int(old_sheet.height / current_tile_height * tile_height),
        ),
    )
    new_pixels = new_sheet.load()

    # copy pixel data while skipping margins
    for tile_x in range(old_sheet.width // current_tile_width):
        for tile_y in range(old_sheet.height // current_tile_height):
            # calculate source tile's position in the old sheet
            src_x_start = tile_x * current_tile_width + tile_margin[0]
            src_y_start = tile_y * current_tile_height + tile_margin[2]
            
            # calculate destination tile's position in the new sheet
            dst_x_start = tile_x * tile_width
            dst_y_start = tile_y * tile_height
            
            # copy pixels within the tile region
            for x in range(tile_width):
                for y in range(tile_height):
                    new_pixels[dst_x_start + x, dst_y_start + y] = old_pixels[
                        src_x_start + x, src_y_start + y
                    ]

    # write out to file and show
    filename = ".".join(filename.split(".")[0:-1]) + "_packed.png"
    new_sheet.save(filename)
    new_sheet.show()


# get int input with retry
def get_int_input(prompt):
    n = input(prompt)
    while not n.isdigit():
        n = input(f"Not a valid number. Try again. {prompt}")
    return int(n)


# user input collection for all values with error detection
def get_all_data(sheet_width, sheet_height):
    print(prompt)
    
    # num rows /cols on the sheet
    print("How many rows and columns are there on the spritesheet?")
    num_cols = get_int_input("  Number of columns: ")
    num_rows = get_int_input("  Number of rows: ")
    # current = (sheet_width // num_cols, sheet_height // num_rows)
    
    # width / height of sheet at start including dimensions
    # print("What are the actual dimensions of the tiles, including margins?")
    # width = get_int_input("  Width: ")
    # height = get_int_input("  Height: ")
    # current = (width, height)

    # actual tile width and height
    print("What are the actual dimensions of the art in the tile, excluding margins?")
    tile_width = get_int_input("  Width: ")
    tile_height = get_int_input("  Height: ")
    future = (tile_width, tile_height)

    # margins around the tile, order l r u d
    print("What are the margins on each side of the art in the file?")
    left_margin = get_int_input("  Left Margin: ")
    right_margin = get_int_input("  Right Margin: ")
    top_margin = get_int_input("  Top Margin: ")
    bottom_margin = get_int_input("  Bottom Margin: ")
    tile_margin = (left_margin, right_margin, top_margin, bottom_margin)

    # current tile width and height
    current_tile_width = tile_width + tile_margin[0] + tile_margin[1]
    current_tile_height = tile_height + tile_margin[2] + tile_margin[3]

    if current_tile_width != sheet_width / num_cols or current_tile_height != sheet_height / num_rows:
        print(
            f"Something isn't quite right. You said the sheet was {num_cols}x{num_rows}, but the tile size with margins based on your inputs is {current_tile_width}x{current_tile_height} and wouldn't fit in the {sheet_width}x{sheet_height} spritesheet. Try again."
        )
        current, future, tile_margin = get_all_data()
    current = (current_tile_width, current_tile_height)
    return current, future, tile_margin


if __name__ == "__main__":
    main()
