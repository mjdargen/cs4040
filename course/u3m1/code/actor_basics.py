# Code atom: creating, positioning, drawing, moving and changing an Actor.
# Quoted by: content/08-content-actors.qmd, u3m1-slides.qmd, u3m1-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "Actor Basics"

# start snippet create
robot = Actor("robot_idle")  # image: images/robot_idle.png
# end snippet create


def start():
    # start snippet position
    robot.pos = (WIDTH // 2, HEIGHT // 2)  # center of the robot
    # end snippet position
    # start snippet anchor
    robot.midbottom = (WIDTH // 2, HEIGHT)  # bottom middle of the robot
    # end snippet anchor
    # start snippet properties
    robot.scale = 2  # twice as large (1 = original, 0.5 = half)
    robot.angle = 45  # rotate 45 degrees counterclockwise
    robot.flip_h = True  # flip horizontally (also flip_v)
    robot.flip_h = False  # turn the flip back off
    # end snippet properties


# start snippet draw
def draw():
    screen.clear()
    robot.draw()  # draw the Actor at its current position
# end snippet draw


# start snippet move
def update():
    robot.x += 1  # move right 1 pixel every frame (~60 per second)
    # end snippet move
    # start snippet image
    if robot.image == "robot_idle":
        robot.image = "robot_jump"
    elif robot.image == "robot_jump":
        robot.image = "robot_idle"
    # end snippet image


pgzrun.go()
