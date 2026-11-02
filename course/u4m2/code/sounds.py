# Code atom: playing short sound effects with sounds.<filename>.<function>().
# Quoted by: u4m2-slides.qmd, u4m2-cheatsheet.qmd
# "thunder" is an example name: this repo has no sounds/ folder, so the name is
# fine as given. To run this, put thunder.wav or thunder.ogg in sounds/.
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 300
TITLE = "Sounds"


def start():
    # start snippet sounds
    sounds.thunder.play()  # plays the sound file called "thunder"
    sounds.thunder.play(10)  # plays "thunder" 10 times
    sounds.thunder.play(-1)  # plays "thunder" forever on a loop
    sounds.thunder.stop()  # stops the "thunder" sound
    sounds.thunder.get_length()  # gets the duration in seconds
    # end snippet sounds


def draw():
    screen.clear()


pgzrun.go()
