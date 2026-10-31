import pgzrun
from pgzero.builtins import *

WIDTH = 800
HEIGHT = 600
TITLE = "Dialogue Example"

# Note: fps is set to 5 below; adjust as needed
crab_idle = Sprite("crab", frame_width=32, frame_height=16, row=0, frames=4, fps=5)
crab_walk = Sprite("crab", frame_width=32, frame_height=16, row=1, frames=4, fps=5)
player = Actor(crab_idle)

# Note: fps is set to 5 below; adjust as needed
frog_idle = Sprite("frog", frame_width=24, frame_height=24, row=0, frames=7, fps=5)
frog_hop = Sprite("frog", frame_width=24, frame_height=24, row=1, frames=8, fps=5)
# Define the Actor
npc = Actor(frog_idle)


# runs once at beginning before draw()/update()
def start():
    player.pos = (200, 200)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    player.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, can't have empty function


pgzrun.go()  # program must always end with this
