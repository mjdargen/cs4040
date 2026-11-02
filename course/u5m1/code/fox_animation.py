# Code atom: controlling an animated Actor (play once, replay, pause).
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# "fox" is a spritesheet in the sprites folder (32 x 32 frames).
import pgzrun
from pgzero.builtins import *

WIDTH = 400
HEIGHT = 300
TITLE = "Controlling Animations"

# start snippet sprites
idle = Sprite("fox", 32, 32, row=0)
attack = Sprite("fox", 32, 32, row=3, loop=False)  # plays once
fox = Actor(idle)
# end snippet sprites


def start():
    fox.pos = (WIDTH // 2, HEIGHT // 2)


def draw():
    screen.clear()
    fox.draw()


def update():
    # start snippet control
    fox.sprite = attack  # same Sprite again: replays only if it has finished
    if fox.animation_finished:  # True once a loop=False Sprite ends
        fox.sprite = idle
    fox.frame  # current frame number, starting at 0
    fox.pause_animation()  # freezes on the current frame
    fox.resume_animation()  # resumes animation on current frame
    # end snippet control


pgzrun.go()
