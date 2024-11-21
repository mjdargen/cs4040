# Sprite Source: https://elthen.itch.io/2d-pixel-art-fox-sprites
import pgzrun
from pgzero.builtins import *
from pgone import *  # must download and import spriteactor.py

# set width and height of screen
WIDTH = 800
HEIGHT = 400
TITLE = "Sprite Actor"

# define global variables
gravity = 1

# example sprite
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
filename = "fox.png"  # Name of file, must be stored in "images" folder
frame_width = 24  # width of each frame
frame_height = 16  # height of each frame
row_number = 1  # row number on the spritesheet
frame_count = 14  # number of frames in the animation
fps = 2  # FPS refresh rate: updates every 2 frames
fox_stand = Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)

# Fox walking animation (walking animation starts at row 2)
row_number = 2  # row number on the spritesheet
frame_count = 8  # Number of frames in the walking animation
fps = 10  # FPS refresh rate: updates every 10 frames
fox_walk = Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)

# define SpriteActor
fox = SpriteActor(fox_stand)
fox.scale = 4  # scales up the Actor size by four

# define Actor-specific variables
fox.velocity_x = 0
fox.velocity_y = 0


# displays the new frame
def draw():
    screen.clear()
    screen.fill("forestgreen")
    fox.draw()


# updates game state between drawing of each frame
def update():
    # while left key is pressed and not at edge
    if keyboard.LEFT and fox.left > 0:
        # flip image and change x velocity
        fox.sprite = fox_walk
        fox.flip_h = True
        fox.velocity_x = -5
    # while right key is pressed and not at edge
    elif keyboard.RIGHT and fox.right < WIDTH:
        # flip image and change x velocity
        fox.sprite = fox_walk
        fox.flip_h = False
        fox.velocity_x = 5
    # otherwise set x velocity to 0
    else:
        fox.velocity_x = 0

    # modify fox position by the velocity
    fox.x += fox.velocity_x
    fox.y += fox.velocity_y

    # handle gravity

    # once the fox has returned to the floor, cancel y velocity
    if fox.bottom >= HEIGHT:
        fox.velocity_y = 0
        fox.y = HEIGHT - fox.height / 2
    # otherwise, continue to add gravity
    # change y velocity by adding gravity
    # causes deceleration in the upwards direction
    # causes acceleration in the downwards direction
    else:
        fox.velocity_y += gravity


# called when a keyboard button is pressed
def on_key_down(key):
    # change vertical velocity when space or up keys are pressed
    # make sure not previously jumping first
    if (key == keys.SPACE or key == keys.UP) and fox.bottom >= HEIGHT:
        fox.velocity_y = -10


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        fox.sprite = fox_stand


pgzrun.go()  # program must always end with this
