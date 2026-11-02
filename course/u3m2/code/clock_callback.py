# Code atom: a clock callback scheduled once in start().
# Based on examples/e08clock.py. Quoted by: u3m2-slides.qmd, u3m2-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *
import random

WIDTH = 500
HEIGHT = 500
TITLE = "Clock Example"

robot = Actor("robot_idle")


# start snippet start
def start():
    robot.pos = (WIDTH // 2, HEIGHT // 2)
    # start snippet schedule
    clock.schedule_interval(move_character, 2.0)  # every 2 seconds
    # end snippet schedule
# end snippet start


def draw():
    screen.clear()
    screen.fill("darkslateblue")
    robot.draw()


# start snippet callback
# scheduled callback for moving character to random position
def move_character():
    robot.x = random.randint(50, WIDTH - 50)
    robot.y = random.randint(50, HEIGHT - 50)
# end snippet callback


pgzrun.go()
