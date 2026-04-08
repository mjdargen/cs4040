import pgzrun
from pgzero.builtins import *
import random

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Clock Example"

# global variables
robot = Actor("robot_idle", (WIDTH // 2, HEIGHT // 2))


# runs once at beginning before draw()/update()
def start():
    clock.schedule_interval(move_character, 2.0)


# displays the new frame
def draw():
    screen.clear()
    screen.fill("darkslateblue")
    robot.draw()
    screen.draw.text(f"Time: {int(game.timer)}", center=(WIDTH // 2, 20))


# updates game state between drawing of each frame
def update():
    pass


# scheduled callback for moving character to a random position
def move_character():
    robot.x = random.randint(50, WIDTH - 50)
    robot.y = random.randint(50, HEIGHT - 50)


pgzrun.go()  # program must always end with this
