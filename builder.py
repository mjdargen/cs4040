import os
from pgzero.builtins import Actor

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def build(filename, tile_size):
    with open(f"{DIR_PATH}/{filename}", "r") as f:
        contents = f.read().splitlines()

    contents = [c.split(",") for c in contents]
    contents = [[int(col) if col.isdigit() else -1 for col in row] for row in contents]

    items = []

    for row in range(len(contents)):
        for col in range(len(contents[0])):
            if contents[row][col] != -1:
                item = Actor(f"tiles/tile_{contents[row][col]:04d}")
                item.topleft = (tile_size * col, tile_size * row)
                items.append(item)

    return items
