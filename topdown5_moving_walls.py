import pgzrun
from pgzero.builtins import *

# tile map scale
MAP_SCALE = 2

# load world from Tiled tile map
level = load_tile_map("topdown_moving_walls.tmx", scale=MAP_SCALE)
ground = level["ground"]
walls = level["walls"]
moving_walls = level["moving_walls"]  # walls that slide back and forth
hazards = level["hazards"]
collectables = level["collectables"]

# Pygame Constants - compute with level dimensions
WIDTH = level.cols * level.tile_width
HEIGHT = level.rows * level.tile_height
TITLE = "Top-Down with Moving Walls"

# define Sprites
idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
walk_down = Sprite("rabbit", frame_width=16, frame_height=16, row=4, frames=2, fps=10)
walk_up = Sprite("rabbit", frame_width=16, frame_height=16, row=5, frames=2, fps=10)
walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=2, fps=10)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16, row=7, frames=2, fps=10)

# define the Actor
rabbit = Actor(idle)

# global variables
# All the tiles in the moving_walls layer move together, in the same direction.
# To have walls that move separately, put them on another layer (like "moving_walls2")
# with its own speed and distance variables, and move it the same way.
wall_speed = 2  # pixels the moving walls move each frame (negative is left)
wall_distance = 0  # how far the moving walls are from where they started


# runs once at beginning before draw()/update()
def start():
    rabbit.scale = MAP_SCALE
    rabbit.midbottom = (WIDTH / 2, HEIGHT - level.tile_height)
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
        # do the same for the moving walls
        collision_index = rabbit.collidelist(moving_walls)
        if collision_index != -1:
            collided_wall = moving_walls[collision_index]
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
        # do the same for the moving walls
        collision_index = rabbit.collidelist(moving_walls)
        if collision_index != -1:
            collided_wall = moving_walls[collision_index]
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
        # do the same for the moving walls
        collision_index = rabbit.collidelist(moving_walls)
        if collision_index != -1:
            collided_wall = moving_walls[collision_index]
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
        # do the same for the moving walls
        collision_index = rabbit.collidelist(moving_walls)
        if collision_index != -1:
            collided_wall = moving_walls[collision_index]
            rabbit.bottom = collided_wall.top

    # otherwise idle
    else:
        rabbit.sprite = idle

    # move the moving walls, which can push the rabbit
    move_walls()

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


# moves the moving walls back and forth, pushing the rabbit if they run into it
def move_walls():
    global wall_speed, wall_distance
    # move every tile in the moving_walls layer
    for tile in moving_walls:
        tile.x += wall_speed
    # if a moving wall ran into the rabbit, push the rabbit along in front of it
    collision_index = rabbit.collidelist(moving_walls)
    if collision_index != -1:
        pushing_wall = moving_walls[collision_index]
        if wall_speed > 0:
            rabbit.left = pushing_wall.right
        else:
            rabbit.right = pushing_wall.left
        # pushed into a wall, so the rabbit is squished, lose
        if rabbit.collidelist(walls) != -1:
            rabbit.alive = False
            game.lose()
    # keep track of how far the walls are from where they started
    wall_distance += wall_speed
    # turn around after moving 128 pixels (4 tiles) away, or when back at the start
    if wall_distance >= 128 or wall_distance <= 0:
        wall_speed = -wall_speed


pgzrun.go()
