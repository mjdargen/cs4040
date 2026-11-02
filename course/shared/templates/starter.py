# program must start with these two lines
import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Name of Game"


# runs once at beginning before draw()/update()
def start():
    pass  # pass means do nothing, can't have empty function


# displays the new frame
def draw():
    pass  # pass means do nothing, can't have empty function


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, can't have empty function


pgzrun.go()  # program must always end with this
