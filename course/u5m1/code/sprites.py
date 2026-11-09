# Code atom: making Sprites (from a list of images and from a sprite sheet)
# and having an Actor play them.
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# Uses images/alien_beige_walk1.png, images/alien_beige_walk2.png and
# sprites/rabbit.png (16 x 16 frames: idle on row 0, walking left and right on rows 6 and 7).
import pgzrun
from pgzero.builtins import *

WIDTH = 400
HEIGHT = 300
TITLE = "Sprites"

# start snippet image_list
# a Sprite made from a list of images in the images folder
alien_walk = Sprite(["alien_beige_walk1", "alien_beige_walk2"], fps=6)
# end snippet image_list

# start snippet sheet
# Sprites made from rows of a sprite sheet in the sprites folder
idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=2, fps=8)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16,row=7, frames=2, fps=8)
# end snippet sheet

# start snippet alien_actor
alien = Actor(alien_walk)  # a Sprite instead of an image name
# end snippet alien_actor
# start snippet rabbit_actor
rabbit = Actor(idle)  # starts by playing idle
rabbit.scale = 3  # pixel art is small, so make it bigger
# end snippet rabbit_actor


def start():
    alien.pos = (100, HEIGHT // 2)
    rabbit.pos = (300, HEIGHT // 2)


def update():
    # start snippet switch
    if keyboard.left:
        rabbit.x -= 2
        rabbit.sprite = walk_left  # switch to another Sprite
    elif keyboard.right:
        rabbit.x += 2
        rabbit.sprite = walk_right
    else:
        rabbit.sprite = idle  # safe every frame: restarts only if it changed
    # end snippet switch


def draw():
    screen.clear()
    alien.draw()  # the Actor moves on to the next frame by itself
    rabbit.draw()


pgzrun.go()
