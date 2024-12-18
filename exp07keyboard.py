import pgzrun
from pgzero.builtins import *

# set width and height of screen
WIDTH = 600
HEIGHT = 300
TITLE = "Keyboard Example"

# define Actors
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.midbottom = (WIDTH // 2, HEIGHT)
robot.velocity_x = 0
robot.velocity_y = 0

# define gravity
gravity = 1


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    robot.draw()


# updates game state between drawing of each frame
def update():
    # while left key is pressed and not at edge
    if keyboard.LEFT and robot.left > 0:
        # show left facing image and change x velocity
        robot.image = "robot_left"
        robot.velocity_x = -5
    # while right key is pressed and not at edge
    elif keyboard.RIGHT and robot.right < WIDTH:
        # show right facing image and change x velocity
        robot.image = "robot_right"
        robot.velocity_x = 5
    # otherwise set x velocity to 0
    else:
        robot.velocity_x = 0

    # modify robot position by the velocity
    robot.x += robot.velocity_x
    robot.y += robot.velocity_y

    # handle gravity
    # once the robot has returned to the floor, cancel y velocity
    if robot.bottom >= HEIGHT:
        robot.velocity_y = 0
        robot.y = HEIGHT - robot.height / 2
    # otherwise, continue to add gravity
    # change y velocity by adding gravity
    # causes deceleration in the upwards direction
    # causes acceleration in the downwards direction
    else:
        robot.velocity_y += gravity


# called when a keyboard button is pressed
def on_key_down(key):
    # change vertical velocity when space or up keys are pressed
    # make sure not previously jumping first
    if (key == keys.SPACE or key == keys.UP) and robot.bottom == HEIGHT:
        robot.velocity_y = -12


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        robot.image = "robot_idle"


pgzrun.go()  # program must always end with this
