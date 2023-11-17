# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
# Sprite Source: https://elthen.itch.io/2d-pixel-art-fox-sprites
import pgzrun  # program must always start with this
from spriteactor import *  # must download and import spriteactor.py

# set width and height of screen
WIDTH = 800
HEIGHT = 400

# define global variables
gravity = 1

# example sprite
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
filename = "fox.png"  # name of file, must be stored in "images" folder
start = (0, 0, 32, 32)  # (x, y, w, h) - x,y of topleft corner, width,height of 1 frame
num_frames = 8  # number of frames in the sprite
color_key = (0, 0, 0)  # leave like this unless background shows up
refresh = 10  # refresh rate - updates every 5 frames
example = Sprite(filename, start, num_frames, color_key, refresh)

# define Sprites
fox_stand = Sprite("fox.png", (0, 32, 32, 32), 14, color_key, 30)
fox_walk = Sprite("fox.png", (0, 2 * 32, 32, 32), 8, color_key, 5)

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
    if keyboard.LEFT and fox.midleft[0] > 0:
        # flip image and change x velocity
        fox.sprite = fox_walk
        fox.flip_x = True
        fox.velocity_x = -5
    # while right key is pressed and not at edge
    elif keyboard.RIGHT and fox.midright[0] < WIDTH:
        # flip image and change x velocity
        fox.sprite = fox_walk
        fox.flip_x = False
        fox.velocity_x = 5
    # otherwise set x velocity to 0
    else:
        fox.velocity_x = 0

    # modify fox position by the velocity
    fox.x += fox.velocity_x
    fox.y += fox.velocity_y

    # handle gravity

    # once the fox has returned to the floor, cancel y velocity
    # fox.midbottom[1] gives bottommost part of actor
    if fox.midbottom[1] >= HEIGHT:
        fox.velocity_y = 0
        fox.midbottom = fox.x, HEIGHT
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
    if (key == keys.SPACE or key == keys.UP) and fox.midbottom[1] == HEIGHT:
        fox.velocity_y = -10


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        fox.sprite = fox_stand


pgzrun.go()  # program must always end with this
