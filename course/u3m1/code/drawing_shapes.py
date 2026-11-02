# Code atom: every screen drawing call used in this module.
# Quoted by: content/04-content-drawing.qmd, u3m1-slides.qmd, u3m1-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 300
TITLE = "Drawing Shapes"


def draw():
    # start snippet fill
    screen.clear()  # removes everything from the window
    screen.fill("darkslateblue")  # fill with a color name
    screen.fill((0, 0, 0))  # or with an RGB tuple
    # end snippet fill
    # start snippet rect
    # screen.draw.rect((x, y), (width, height), "color")
    screen.draw.rect((0, 0), (100, 200), "blue")  # outlined rectangle
    # screen.draw.filled_rect((x, y), (width, height), "color")
    screen.draw.filled_rect((25, 50), (50, 80), "red")  # filled rectangle
    # end snippet rect
    # start snippet line
    # screen.draw.line((x1, y1), (x2, y2), "color")
    screen.draw.line((0, 0), (100, 100), "purple")
    # end snippet line
    # start snippet circle
    # screen.draw.circle((x, y), radius, "color")
    screen.draw.circle((250, 150), 60, "purple")  # outlined circle
    # screen.draw.filled_circle((x, y), radius, "color")
    screen.draw.filled_circle((120, 120), 40, "red")  # filled circle
    # end snippet circle
    # start snippet text
    screen.draw.text("hello", (20, 200))  # top-left corner at (20, 200)
    screen.draw.text("hello", (100, 100), fontsize=32)
    screen.draw.text("hello", (0, 100), fontsize=32, color="orange")
    screen.draw.text("hello world", centery=50, right=300)
    screen.draw.text("BARK!", midtop=(400, 0), color="red")
    # end snippet text


pgzrun.go()
