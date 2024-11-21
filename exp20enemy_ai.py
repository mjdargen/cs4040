import pgzrun
from pgzero.builtins import *

# Pygame constants
WIDTH = 400
HEIGHT = 400
TITLE = "Enemy AI Demo"

enemy = Actor("alien_yellow")
enemy.bottomleft = (100, HEIGHT)
enemy.velocity_x = 5


# displays the new frame
def draw():
    screen.clear()
    screen.fill("forestgreen")
    enemy.draw()


# updates game state between drawing of each frame
def update():
    pass


# callback function for moving enemy with "AI"
def move_enemy():
    enemy.x += enemy.velocity_x
    # move back and forth between 100 and 300
    if enemy.x >= 300:
        enemy.velocity_x = -5
    if enemy.x <= 100:
        enemy.velocity_x = 5

# schedule move enemy to happen every 0.01 seconds at start or elsewhere
clock.schedule_interval(move_enemy, .01)
pgzrun.go()