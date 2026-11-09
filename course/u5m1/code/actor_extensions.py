# Code atom: extra Actor features in the course's Pygame Zero fork.
# Quoted by: u5m1-slides.qmd, u5m1-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "Actor Extensions"

player = Actor("player_blue_stand")


def start():
    player.pos = (WIDTH // 2, HEIGHT // 2)
    # start snippet extensions
    player.angle  # gets current angle in degrees
    player.angle += 1  # increments angle by 1
    player.scale  # gets current Actor scaling factor
    player.scale = 2.0  # sets the Actor scaling factor
    player.flip_v = True  # flips the Actor vertically
    player.flip_v = False  # turns off vertical flip, default
    player.flip_h = True  # flips the Actor horizontally
    player.flip_h = False  # turns off horizontal flip, default
    # end snippet extensions
    # start snippet visibility
    player.opacity = 0.6  # sets opacity, from 0.0 to 1.0
    player.visible = False  # hides it; still moves and collides
    # end snippet visibility
    # start snippet collision_rect
    player.collision_rect = (10, 20)  # (width, height)
    # (width, height, offset_x, offset_y)
    player.collision_rect = (50, 20, 5, -5)
    # end snippet collision_rect


def draw():
    screen.clear()
    player.draw()
    # start snippet debug_rect
    player.draw_collision_rect()  # outlines it in red, for debugging
    # end snippet debug_rect


pgzrun.go()
