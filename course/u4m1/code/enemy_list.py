# Code atom: a list of enemy Actors spawned on a timer, drawn and moved with
# for loops, plus collidelist() collisions with enemies and collectible gems.
# Quoted by: u4m1-slides.qmd, u4m1-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *
import random

WIDTH = 500
HEIGHT = 500
TITLE = "Lists of Actors"

# set-up so this example runs (not shown on the slides)
player = Actor("player_blue_stand", (250, 400))
gems = [
    Actor("gem_blue", (100, 300)),
    Actor("gem_green", (250, 200)),
    Actor("gem_red", (400, 300)),
]

# start snippet program
# start snippet spawn
# globals
enemies = []


# runs once at beginning
def start():
    enemies.clear()
    clock.schedule_interval(spawn_enemy, 5)


# create spawn callback function
def spawn_enemy():
    enemy = Actor("alien")
    enemy.pos = (100, 100)
    enemy.velocity_x = random.randint(1, 5)
    enemy.velocity_y = random.randint(1, 5)
    enemies.append(enemy)
# end snippet spawn


# start snippet draw
def draw():
    screen.clear()
    for enemy in enemies:  # one Actor at a time, in order
        enemy.draw()
    # end snippet draw
    for gem in gems:
        gem.draw()
    player.draw()


# start snippet move
def update():
    for enemy in enemies:  # each Actor moves by its own velocity
        enemy.x += enemy.velocity_x
        enemy.y += enemy.velocity_y
    # end snippet move

    # start snippet collide
    # check for enemy collision with list
    if player.collidelist(enemies) != -1:  # -1 means no collision
        game.lose()  # game over

    # check for collectible collision with list
    collision_index = player.collidelist(gems)  # index of the gem hit
    if collision_index != -1:
        # collected gem, remove from list
        gems.pop(collision_index)
        game.score += 1
    # end snippet collide
# end snippet program


# move the player with the mouse (not shown on the slides)
def on_mouse_move(pos):
    player.pos = pos


pgzrun.go()
