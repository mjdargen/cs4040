# requires Python Image Library or Pillow: https://pypi.org/project/Pillow/
# most run command to install: "pip install Pillow"
import os
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename


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
    # filename = "frog_idle.png"
    # load old sheet
    old_sheet = Image.open(filename)
    old_pixels = old_sheet.load()

    # input
    # current, future, tile_margin = get_all_data()
    # tile_width, tile_height = future
    # current_tile_width, current_tile_height = current

    # hardcoded
    tile_width = 24
    tile_height = 16
    # l r t b
    tile_margin = [12, 12, 16, 16]
    current_tile_width = tile_width + tile_margin[0] + tile_margin[1]
    current_tile_height = tile_height + tile_margin[2] + tile_margin[3]

    # create new sheet
    new_sheet = Image.new(
        "RGBA",
        (
            old_sheet.width // current_tile_width * tile_width,
            old_sheet.height // current_tile_height * tile_height,
        ),
    )
    new_pixels = new_sheet.load()
    image_data = []  # structure for storing pixel data not in margins

    # get old data - skip when on margins
    for x in range(old_sheet.width):
        _x = x % 32
        if _x < tile_margin[0] or _x >= current_tile_width - tile_margin[1]:
            continue
        for y in range(old_sheet.height):
            _y = y % 32
            if _y < tile_margin[2] or _y >= current_tile_height - tile_margin[3]:
                continue
            image_data.append(old_pixels[x, y])

    # place image data in new image
    for x in range(new_sheet.width):
        for y in range(new_sheet.height):
            new_pixels[x, y] = image_data[x * new_sheet.height + y]

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
def get_all_data():
    # width / height of sheet at start including dimensions
    print("What are the actual dimensions of the tiles, including margins?")
    width = get_int_input("  Width: ")
    height = get_int_input("  Height: ")
    current = (width, height)

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

    if current_tile_width != width or current_tile_height != height:
        print(
            f"Something isn't quite right. You said the original tile was {width}x{height}, but your parameters add up to {current_tile_width}x{current_tile_height}. Try again."
        )
        current, future, tile_margin = get_all_data()

    return current, future, tile_margin


if __name__ == "__main__":
    main()
