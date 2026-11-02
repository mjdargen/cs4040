# Code atom: event-based input (on_key_down) vs. polling input (update).
# Quoted by: u3m2-slides.qmd, u3m2-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "Events vs. Polling"

player = Actor("alien_green")


def start():
    player.pos = (WIDTH // 2, HEIGHT // 2)


def draw():
    screen.clear()
    player.draw()


# start snippet event
def on_key_down(key):
    if key == keys.UP:  # up key pressed
        player.y -= 10  # once per press
# end snippet event


# start snippet polling
def update():
    if keyboard.d:  # D key held down
        player.x += 1  # every frame
# end snippet polling


pgzrun.go()
