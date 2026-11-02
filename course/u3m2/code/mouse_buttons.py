# Code atom: the mouse button constants and a mouse event listener.
# Quoted by: u3m2-slides.qmd, u3m2-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "Mouse Buttons"


def start():
    # start snippet buttons
    mouse.LEFT  # left button
    mouse.MIDDLE  # middle button
    mouse.RIGHT  # right button
    mouse.WHEEL_UP  # scroll up
    mouse.WHEEL_DOWN  # scroll down
    # end snippet buttons


def draw():
    screen.clear()


# start snippet listener
def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        print("Left mouse button clicked.")
    elif button == mouse.RIGHT:
        print("Right mouse button clicked.")
    else:
        print("Other mouse button clicked.")
# end snippet listener


pgzrun.go()
