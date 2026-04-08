import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Collision Box Resizing Demo"

# Define a Sprite and SpriteActor
filename = "fox.png"  # Name of file, must be stored in "images" folder
frame_width = 24  # width of each frame
frame_height = 16  # height of each frame
row_number = 1  # row number on the spritesheet
frame_count = 14  # number of frames in the animation
fps = 2  # FPS refresh rate: updates every 2 frames
fox_stand = Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)

# define SpriteActor
player = SpriteActor(fox_stand)
player.pos = (WIDTH / 2, 300)
player.scale = 2
# specify offset_x, offset_y from center and width, height
player.collision_rect = (2, 4, 16, 8)

# Create two actors with different collision rectangles
enemy1 = Actor("alien_yellow", (100, 200))
# specify width and height of new box - centered at image center
enemy1.collision_rect = (40, 80)
enemy2 = Actor("alien_blue", (400, 200))
# OR specify offset_x, offset_y from center and width, height
enemy2.collision_rect = (0, 20, 40, 50)


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
