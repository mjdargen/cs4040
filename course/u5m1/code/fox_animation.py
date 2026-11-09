# Code atom: controlling an animated Actor (play once, check, pause, jump to a frame).
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
# "fox" is a sprite sheet in the sprites folder (24 x 16 frames: idle on row 0, hurt on row 4).
# Space: get hurt. P: pause or resume. R: restart the animation.
import pgzrun
from pgzero.builtins import *

WIDTH = 400
HEIGHT = 300
TITLE = "Controlling Animations"

# start snippet sprites
idle = Sprite("fox", frame_width=24, frame_height=16,
              row=0, frames=5, fps=6)
hurt = Sprite("fox", frame_width=24, frame_height=16,
              row=4, frames=5, fps=8, loop=False)  # plays once
fox = Actor(idle)
# end snippet sprites


def start():
    fox.scale = 4
    fox.pos = (WIDTH // 2, HEIGHT // 2)


# start snippet keys
def on_key_down(key):
    if key == keys.SPACE:
        fox.sprite = hurt  # replays if it has already finished
    if key == keys.P:
        if fox.animation_paused:  # True while paused
            fox.resume_animation()  # carry on from the same frame
        else:
            fox.pause_animation()  # freeze on the current frame
    if key == keys.R:
        fox.reset_animation()  # play again from the first frame
# end snippet keys


def update():
    # start snippet play_once
    if fox.sprite == hurt and fox.animation_finished:  # hurt has ended
        fox.sprite = idle  # go back to idle
    # end snippet play_once


def draw():
    screen.clear()
    fox.draw()
    # start snippet frame
    screen.draw.text(f"frame {fox.frame}", (10, 10))  # frame number, from 0
    # end snippet frame


pgzrun.go()
