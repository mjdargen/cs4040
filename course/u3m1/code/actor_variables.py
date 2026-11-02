# Code atom: Actor variables (our own variables attached to an Actor).
# Quoted by: content/10-content-actor-variables.qmd, u3m1-slides.qmd, u3m1-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500

# start snippet program
alien = Actor("alien_beige")


# start snippet start
def start():
    alien.pos = (0, 500)  # pos is built in
    alien.velocity_x = 1  # velocity_x is ours
    alien.velocity_y = -1  # velocity_y is ours
# end snippet start


def draw():
    screen.clear()
    alien.draw()


# start snippet update
def update():
    alien.x += alien.velocity_x
    alien.y += alien.velocity_y
# end snippet update
# end snippet program


pgzrun.go()
