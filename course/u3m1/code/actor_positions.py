# Code atom: every way to read or set an Actor's position.
# Quoted by: u3m1-cheatsheet.qmd, u3m1-slides.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500

alien = Actor("alien")


def start():
    # start snippet single
    # one coordinate, an int: get or set
    alien.x  # center x
    alien.y  # center y
    alien.top  # top edge y (smallest y)
    alien.bottom  # bottom edge y (largest y)
    alien.left  # left edge x (smallest x)
    alien.right  # right edge x (largest x)
    alien.width  # width in pixels (read only)
    alien.height  # height in pixels (read only)
    # end snippet single
    # start snippet pairs
    # a point, an (x, y) tuple: get or set
    alien.pos = (100, 50)  # center
    alien.topleft = (10, 10)  # top-left corner
    alien.midright = (20, 20)  # middle of the right edge
    alien.midtop  # also midbottom, topright, bottomleft...
    # end snippet pairs
    # start snippet move
    alien.x += 1  # move right 1 pixel
    alien.x -= 1  # move left 1 pixel
    alien.y += 1  # move down 1 pixel
    alien.y -= 1  # move up 1 pixel
    # end snippet move


def draw():
    screen.clear()
    alien.draw()


pgzrun.go()
