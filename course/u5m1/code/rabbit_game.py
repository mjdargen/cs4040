# Code atom: a tilemap game with an animated rabbit that stops at walls.
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# Needs sprites/rabbit.png (16 x 16 frames) and maps/L1.tmx made in Tiled,
# with layers named ground, walls, hazards and hearts.
import pgzrun
from pgzero.builtins import *

# start snippet constants
# our tile map constants
TILE_SIZE = 18  # length of a tile, in pixels
MAP_WIDTH = 30  # width of the tilemap, in tiles
MAP_HEIGHT = 20  # height of the tilemap, in tiles
SCALE = 2  # global scaling factor
# can use to compute screen dimensions
WIDTH = TILE_SIZE * MAP_WIDTH * SCALE
HEIGHT = TILE_SIZE * MAP_HEIGHT * SCALE
# end snippet constants
TITLE = "Rabbit Tilemap"

# start snippet sprites
# define Sprites
# start snippet idle
idle = Sprite("rabbit", frame_width=16, frame_height=16,
              row=0, frames=2, fps=3)
# end snippet idle
# start snippet walk_sprites
walk_left = Sprite("rabbit", frame_width=16, frame_height=16,
                   row=6, frames=2, fps=10)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16,
                    row=7, frames=2, fps=10)
# end snippet walk_sprites

# start snippet actor
# make an Actor that plays a Sprite
rabbit = Actor(idle)
# end snippet actor
# end snippet sprites

# start snippet layers
map_layers = load_tile_map_actors("L1.tmx", scale=SCALE)
ground = map_layers["ground"]  # ground / background scenery to draw
walls = map_layers["walls"]  # obstacles for player to collide with
hazards = map_layers["hazards"]  # "bad" objects for player collision
hearts = map_layers["hearts"]  # "good" objects or collectables
# end snippet layers


def start():
    rabbit.scale = SCALE
    rabbit.pos = (WIDTH // 2, HEIGHT // 2)


def draw():
    screen.clear()
    for tile in ground + walls + hazards + hearts:
        tile.draw()
    rabbit.draw()


def update():
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
    if keyboard.RIGHT:
        # start snippet switch
        rabbit.sprite = walk_right
        # end snippet switch
        rabbit.x += 2
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            rabbit.right = walls[collision_index].left


pgzrun.go()
