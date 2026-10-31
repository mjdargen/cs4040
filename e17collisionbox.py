import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Collision Box Resizing Demo"

# Define a Sprite and an Actor
fox_stand = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=2)

# define actors
player = Actor(fox_stand)
enemy1 = Actor("alien_yellow")
enemy2 = Actor("alien_blue")


def start():
    player.pos = (WIDTH / 2, 300)
    player.scale = 2
    enemy1.pos = (100, 200)
    enemy2.pos = (400, 200)
    # specify offset_x, offset_y from center and width, height
    player.collision_rect = (16, 8, 2, 4)
    # specify width and height of new box - centered at image center
    enemy1.collision_rect = (40, 80)
    # OR specify offset_x, offset_y from center and width, height
    enemy2.collision_rect = (40, 50, 0, 20)


def draw():
    screen.clear()

    # Draw actors normally
    player.draw()
    enemy1.draw()
    enemy2.draw()

    # Draw collision rectangles for debugging
    player.draw_collision_rect()
    enemy1.draw_collision_rect()
    enemy2.draw_collision_rect()

    # Check and display collision status
    if player.colliderect(enemy1):
        screen.draw.text(
            "Enemy 1 collision!",
            center=(WIDTH / 2, 50),
            color="red",
            fontsize=30,
        )
    elif player.colliderect(enemy2):
        screen.draw.text(
            "Enemy 2 collision!",
            center=(WIDTH / 2, 50),
            color="red",
            fontsize=30,
        )
    else:
        screen.draw.text("No collision", center=(WIDTH / 2, 50), color="green", fontsize=30)


def update():
    # Simple keyboard movement for player
    if keyboard.left:
        player.x -= 5
    if keyboard.right:
        player.x += 5
    if keyboard.up:
        player.y -= 5
    if keyboard.down:
        player.y += 5


pgzrun.go()
