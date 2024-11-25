import pgzrun
from pgzero.builtins import *
from pgone import *

WIDTH = 500
HEIGHT = 500
TITLE = "Collision Boc Resizing Demo"

# Create two actors with different collision rectangles
player = Actor("alien_beige", (WIDTH / 2, 300))
enemy1 = Actor("alien_yellow", (100, 200))
# specify width and height of new box - centered at image center
enemy1.collision_rect = (40, 80)
enemy2 = Actor("alien_blue", (400, 200))
# OR specify distance from center to top, right, bottom, left edge
enemy2.collision_rect = (30, 20, 50, 20)


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
        screen.draw.text("Enemy 1 collision!", center=(WIDTH / 2, 50), color="red", fontsize=30)
    elif player.colliderect(enemy2):
        screen.draw.text("Enemy 2 collision!", center=(WIDTH / 2, 50), color="red", fontsize=30)
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
