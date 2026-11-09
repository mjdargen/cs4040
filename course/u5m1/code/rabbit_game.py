# Code atom: a tilemap game: an animated rabbit that stops at walls, collects
# items and loses on hazards.
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# Needs sprites/rabbit.png (16 x 16 frames) and maps/tl1.tmx made in Tiled,
# with layers named ground, walls, hazards and collectables.
import pgzrun
from pgzero.builtins import *

# start snippet constants
# our tile map constants
TILE_SIZE = 16  # length of a tile, in pixels
MAP_WIDTH = 30  # width of the tilemap, in tiles
MAP_HEIGHT = 20  # height of the tilemap, in tiles
SCALE = 2  # global scaling factor
# can use to compute screen dimensions
WIDTH = TILE_SIZE * MAP_WIDTH * SCALE
HEIGHT = TILE_SIZE * MAP_HEIGHT * SCALE
# end snippet constants
TITLE = "Rabbit Tilemap"

idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=2, fps=8)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16, row=7, frames=2, fps=8)
rabbit = Actor(idle)

# start snippet layers
level = load_tile_map("tl1.tmx", scale=SCALE)
ground = level["ground"]  # ground / background scenery to draw
walls = level["walls"]  # obstacles for player to collide with
hazards = level["hazards"]  # "bad" objects for player collision
collectables = level["collectables"]  # "good" objects to collect
# end snippet layers


def start():
    rabbit.scale = SCALE
    rabbit.pos = (200, HEIGHT // 2)


def draw():
    screen.clear()
    # start snippet draw
    level.draw()  # draws every visible layer, in Tiled's layer order
    rabbit.draw()  # draw the player after the map, so it is on top
    # end snippet draw
    if game.state == "lost":
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2))
    elif game.state == "won":
        screen.draw.text("You win!", center=(WIDTH // 2, HEIGHT // 2))


def update():
    if game.state != "playing":
        return

    # start snippet wall_collision
    # left keyboard button pressed
    if keyboard.LEFT:
        rabbit.x -= 2  # move to left
        rabbit.sprite = walk_left  # change to left sprite
        # check for collision
        collision_index = rabbit.collidelist(walls)
        # did collision occur after moving to left?
        if collision_index != -1:
            # if so, put character's left edge on right edge of wall
            rabbit.left = walls[collision_index].right
    # end snippet wall_collision
    elif keyboard.RIGHT:
        rabbit.x += 2
        rabbit.sprite = walk_right
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            rabbit.right = walls[collision_index].left
    elif keyboard.UP:
        rabbit.y -= 2
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            rabbit.top = walls[collision_index].bottom
    elif keyboard.DOWN:
        rabbit.y += 2
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            rabbit.bottom = walls[collision_index].top
    else:
        rabbit.sprite = idle

    # start snippet collect
    # touching a collectable? take it off the map
    item_index = rabbit.collidelist(collectables)
    if item_index != -1:
        collectables.pop(item_index)
    # collected them all?
    if len(collectables) == 0:
        game.win()
    # end snippet collect

    # start snippet hazard
    # touching any hazard ends the game
    if rabbit.collidelist(hazards) != -1:
        game.lose()
    # end snippet hazard


pgzrun.go()
