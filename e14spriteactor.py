# Sprite Source: https://elthen.itch.io/2d-pixel-art-fox-sprites
import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 800
HEIGHT = 400
TITLE = "Sprite Actor"

# A Sprite is one animation cut from a sprite sheet:
#   "fox"            name of the sprite sheet, stored in the "sprites" folder
#   frame_width      width of each frame, in pixels
#   frame_height     height of each frame, in pixels
#   row              which row of the sheet the animation is on (top row is 0)
#   frames           number of frames in the animation
#   fps              how many frames to show each second

# Fox idle animation (row 1, shows ~2 frames per second)
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=2)

# Fox walking animation (row 2, shows ~10 frames per second)
fox_walk = Sprite("fox", frame_width=24, frame_height=16, row=2, frames=8, fps=10)

# define the Actor
fox = Actor(fox_idle)

# A Sprite can also be made from a list of images in the "images" folder.
# The bee flaps its wings by switching between two images, 8 times a second.
bee_fly = Sprite(["bee_a", "bee_b"], fps=8)

# define the bee Actor
bee = Actor(bee_fly)


# runs once at beginning before draw()/update()
def start():
    fox.scale = 4  # scales up the Actor size by four
    fox.bottomleft = (0, HEIGHT)
    fox.velocity_x = 0
    bee.pos = (WIDTH / 2, 80)
    bee.velocity_x = -3  # the bee starts flying left


# displays the new frame
def draw():
    screen.clear()
    screen.fill("forestgreen")
    fox.draw()
    bee.draw()


# updates game state between drawing of each frame
def update():
    # while left key is pressed and not at edge
    if keyboard.left and fox.left > 0:
        # flip image and change x velocity
        fox.sprite = fox_walk
        fox.flip_h = True
        fox.velocity_x = -5
    # while right key is pressed and not at edge
    elif keyboard.right and fox.right < WIDTH:
        # flip image and change x velocity
        fox.sprite = fox_walk
        fox.flip_h = False
        fox.velocity_x = 5
    # otherwise set x velocity to 0
    else:
        fox.velocity_x = 0

    # modify fox position by the velocity
    fox.x += fox.velocity_x

    # fly the bee back and forth, turning around at the edges of the screen
    bee.x += bee.velocity_x
    if bee.left < 0 or bee.right > WIDTH:
        bee.velocity_x = -bee.velocity_x
    # the bee images face left, so flip them when the bee flies right
    bee.flip_h = bee.velocity_x > 0


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        fox.sprite = fox_idle


pgzrun.go()  # program must always end with this
