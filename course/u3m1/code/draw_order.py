# Code atom: window constants + drawing order.
# Quoted by: content/04-content-drawing.qmd, u3m1-slides.qmd
import pgzrun
from pgzero.builtins import *

# start snippet constants
# Pygame Zero constants
WIDTH = 712
HEIGHT = 508
TITLE = "Demo Game"
# end snippet constants


# start snippet draw
def draw():
    # runs top to bottom, so draw back to front
    screen.clear()  # remove the previous frame
    screen.fill("darkslateblue")  # background first
    screen.draw.filled_circle((100, 100), 50, "red")
    screen.draw.filled_circle((125, 125), 25, "yellow")  # drawn last, so on top
# end snippet draw


pgzrun.go()
