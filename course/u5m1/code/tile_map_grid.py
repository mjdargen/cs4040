# Code atom: changing a tile map with code: creating, adding and removing
# tiles, changing a tile's image, and converting between pixels and squares.
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# Uses maps/tl1.tmx (layers ground, walls, hazards and collectables; one tileset,
# where image col 3, row 8 and image col 4, row 8 are walls) and sprites/rabbit.png.
# Click to build or knock down walls.
import pgzrun
from pgzero.builtins import *

TILE_SIZE = 16
MAP_WIDTH = 30
MAP_HEIGHT = 20
SCALE = 2
WIDTH = TILE_SIZE * MAP_WIDTH * SCALE
HEIGHT = TILE_SIZE * MAP_HEIGHT * SCALE
TITLE = "Tile Map Grid"

level = load_tile_map("tl1.tmx", scale=SCALE)
walls = level["walls"]
hazards = level["hazards"]
items = level["collectables"]

idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
rabbit = Actor(idle, scale=SCALE)


def crash_example():
    # never called: shows the mistake that "if wall:" prevents
    # start snippet crash
    wall = walls.get_tile(0, 0)  # an empty square, so wall is None
    wall.set_tile_image(4, 8)  # crash! None has no set_tile_image()
    # end snippet crash


def map_reference(x, y, col, row):
    # never called: what you can do with the map
    # start snippet map_ref
    walls = level["walls"]  # get a layer by its name in Tiled
    level.draw()  # draw every visible layer
    new_wall = level.create_tile(3, 8)  # create a tile from the tileset
    col, row = level.pos_to_map(x, y)  # pixels -> square
    x, y = level.map_to_pos(col, row)  # square -> pixels (its center)
    level.x -= 3  # scroll the whole map
    # end snippet map_ref


def layer_reference(col, row, new_wall):
    # never called: what you can do with a layer
    # start snippet layer_ref
    first = walls[0]  # it's a list of tiles: [i], len(), for loops
    index = rabbit.collidelist(walls)  # collisions work like any list
    walls.pop(index)  # remove a tile by its index
    wall = walls.get_tile(col, row)  # the tile in a square, or None
    walls.set_tile(col, row, new_wall)  # put a tile in a square
    walls.remove_tile(col, row)  # empty a square
    walls.visible = False  # stop drawing it (it still collides)
    # end snippet layer_ref


def tile_reference(wall):
    # never called: what you can do with a tile
    # start snippet tile_ref
    wall.pos  # it's an Actor: pos, x, y, colliderect(), ...
    wall.map_col, wall.map_row  # its square on the map
    wall.tile_col, wall.tile_row  # its image in the tileset
    wall.set_tile_image(4, 8)  # show another image from the tileset
    # end snippet tile_ref


def grid_examples():
    # start snippet find
    wall = walls.get_tile(2, 5)  # a tile, or None if the square is empty
    if wall:  # only if there is a tile there
        print(wall.map_col, wall.map_row)  # every tile knows its square
    # end snippet find

    # start snippet create
    # a new tile showing the image at col 3, row 8 of the tileset
    new_wall = level.create_tile(3, 8)
    # end snippet create

    # start snippet add
    walls.set_tile(5, 2, new_wall)  # put it at col 5, row 2 of the map
    # end snippet add

    # start snippet remove
    walls.remove_tile(5, 2)  # take away the tile at col 5, row 2, if any
    # end snippet remove

    # start snippet image
    wall = walls.get_tile(2, 5)  # find the tile at col 2, row 5
    if wall:
        wall.set_tile_image(4, 8)  # show image col 4, row 8 instead
    # end snippet image


def start():
    grid_examples()
    # start snippet map_to_pos
    rabbit.pos = level.map_to_pos(5, 9)  # middle of col 5, row 9
    # end snippet map_to_pos


# start snippet click
def on_mouse_down(pos):
    x, y = pos
    col, row = level.pos_to_map(x, y)  # the square that was clicked
    if walls.get_tile(col, row):  # is there a wall?
        walls.remove_tile(col, row)  # knock it down
    else:
        walls.set_tile(col, row, level.create_tile(3, 8))  # build one
# end snippet click


def update():
    old_pos = rabbit.pos
    if keyboard.left:
        rabbit.x -= 2
    if keyboard.right:
        rabbit.x += 2
    if keyboard.up:
        rabbit.y -= 2
    if keyboard.down:
        rabbit.y += 2
    if rabbit.collidelist(walls) != -1:
        rabbit.pos = old_pos  # don't walk through walls

    # start snippet pos_to_map
    col, row = level.pos_to_map(rabbit.x, rabbit.y)  # rabbit's square
    # end snippet pos_to_map

    item_index = rabbit.collidelist(items)
    if item_index != -1:
        items.pop(item_index)


def draw():
    screen.clear()
    level.draw()
    rabbit.draw()


pgzrun.go()
