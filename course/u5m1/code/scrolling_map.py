# Code atom: a map bigger than the screen that scrolls as the player walks.
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# Uses maps/topdown_open_world.tmx (layers ground, walls, collectables and hazards)
# and sprites/rabbit.png.
import pgzrun
from pgzero.builtins import *

WIDTH = 640
HEIGHT = 480
TITLE = "Scrolling Map"

level = load_tile_map_actors("topdown_open_world.tmx", scale=2)
walls = level["walls"]

idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
rabbit = Actor(idle, scale=2, pos=(WIDTH // 2, HEIGHT // 2))


# start snippet scroll
def update():
    old_x, old_y = level.x, level.y
    if keyboard.left:
        level.x += 3  # move the map right, so the rabbit seems to walk left
    if keyboard.right:
        level.x -= 3
    if keyboard.up:
        level.y += 3
    if keyboard.down:
        level.y -= 3
    if rabbit.collidelist(walls) != -1:
        level.x, level.y = old_x, old_y  # hit a wall: put the map back
# end snippet scroll


def draw():
    screen.clear()
    level.draw()
    rabbit.draw()


pgzrun.go()
