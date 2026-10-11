# program must start with these two lines
import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 500  # width of game window
HEIGHT = 500  # height of game window
TITLE = "Name of Game"  # title in game window

# define global variables
alien = Actor("alien")


# runs once at beginning before draw()/update()
def start():
    alien.pos = (200, 200)  # sets initial position


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, can't have empty function


pgzrun.go()  # program must always end with this
