import pgzrun
from pgzero.builtins import *

# our tile map constants
TILE_SIZE = 16
MAP_WIDTH = 30
MAP_HEIGHT = 20
SCALE = 2

# Pygame Constants
WIDTH = TILE_SIZE * MAP_WIDTH * SCALE
HEIGHT = TILE_SIZE * MAP_HEIGHT * SCALE
TITLE = "Top-Down"

# build world from Tiled tile map
level = load_tile_map("topdown.tmx", scale=SCALE)
ground = level["ground"]
walls = level["walls"]
hazards = level["hazards"]
collectables = level["collectables"]

# define Sprites
idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
walk_down = Sprite("rabbit", frame_width=16, frame_height=16, row=4, frames=2, fps=10)
walk_up = Sprite("rabbit", frame_width=16, frame_height=16, row=5, frames=2, fps=10)
walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=2, fps=10)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16, row=7, frames=2, fps=10)

# define the Actor
rabbit = Actor(idle)


# runs once at beginning before draw()/update()
def start():
    rabbit.scale = SCALE
    rabbit.midbottom = (WIDTH / 2, HEIGHT - TILE_SIZE * SCALE)
    rabbit.alive = True
    rabbit.velocity = 4


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    # draw every layer of the tile map, in the order Tiled shows them
    level.draw()
    # draw the rabbit if still alive
    if rabbit.alive:
        rabbit.draw()

    # draw messages over top
    if game.state == "lost":
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2))
    elif game.state == "won":
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))


# updates game state between drawing of each frame
def update():
    # if game state is not playing, just return
    if game.state != "playing":
        return

    # handle rabbit left movement
    if keyboard.LEFT:
        # change x position and sprite
        rabbit.x -= rabbit.velocity
        rabbit.sprite = walk_left
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.left = collided_wall.right

    # handle rabbit right movement
    elif keyboard.RIGHT:
        # change x position and sprite
        rabbit.x += rabbit.velocity
        rabbit.sprite = walk_right
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.right = collided_wall.left

    # handle rabbit up movement
    elif keyboard.UP:
        # change y position and sprite
        rabbit.y -= rabbit.velocity
        rabbit.sprite = walk_up
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.top = collided_wall.bottom

    # handle rabbit down movement
    elif keyboard.DOWN:
        # change y position and sprite
        rabbit.y += rabbit.velocity
        rabbit.sprite = walk_down
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.bottom = collided_wall.top

    # otherwise idle
    else:
        rabbit.sprite = idle

    # rabbit collided with hazard, lose
    if rabbit.collidelist(hazards) != -1:
        rabbit.alive = False
        game.lose()

    # check if rabbit collected collectables
    heart_index = rabbit.collidelist(collectables)
    if heart_index != -1:
        collectables.pop(heart_index)

    # check if rabbit collected all collectables
    if len(collectables) == 0:
        game.win()


pgzrun.go()  # program must always end with this
