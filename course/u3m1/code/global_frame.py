# Code atom: a global frame counter.
# Quoted by: content/06-content-global-variables.qmd, u3m1-slides.qmd, u3m1-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500

# start snippet program
alien = Actor("alien_green")
frame = 0  # global variable: how many frames so far


def start():
    alien.pos = (0, 250)


def draw():
    screen.clear()
    alien.draw()


# start snippet update
def update():
    global frame  # we reassign frame, so we need global
    frame += 1
    if frame % 10 == 0:  # every 10 frames
        alien.x += 1
# end snippet update
# end snippet program


pgzrun.go()
