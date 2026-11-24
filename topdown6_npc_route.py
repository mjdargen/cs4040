import pgzrun
from pgzero.builtins import *

# tile map scale
MAP_SCALE = 2

# load world from Tiled tile map
level = load_tile_map("topdown.tmx", scale=MAP_SCALE)
ground = level["ground"]
walls = level["walls"]
hazards = level["hazards"]
collectables = level["collectables"]

# Pygame Constants - compute with level dimensions
WIDTH = level.cols * level.tile_width
HEIGHT = level.rows * level.tile_height
TITLE = "Top-Down NPC Route"

# define Sprites
idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
walk_down = Sprite("rabbit", frame_width=16, frame_height=16, row=4, frames=2, fps=10)
walk_up = Sprite("rabbit", frame_width=16, frame_height=16, row=5, frames=2, fps=10)
walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=2, fps=10)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16, row=7, frames=2, fps=10)
dog_walk = Sprite("dog_pixelboy", frame_width=16, frame_height=16, row=0, frames=2, fps=5)

# define the Actors
rabbit = Actor(idle)
dog = Actor(dog_walk)  # an NPC (non-player character) that walks around on its own


# runs once at beginning before draw()/update()
def start():
    rabbit.scale = MAP_SCALE
    rabbit.midbottom = (WIDTH / 2, HEIGHT - level.tile_height)
    rabbit.alive = True
    rabbit.velocity = 4
    dog.scale = MAP_SCALE
    dog.velocity = 2
    # the dog's route: the squares where it turns, as (column, row),
    # found by hovering over the map in Tiled. It walks a loop in the middle,
    # on squares with no items or hazards, so it doesn't walk over them.
    dog.route = [(12, 5), (19, 5), (19, 9), (12, 9)]
    dog.next_stop = 0  # index of the square in the route it's walking to
    # start the dog on the first square of its route
    col, row = dog.route[0]
    dog.pos = level.map_to_pos(col, row)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    # draw every layer of the tile map, in the order Tiled shows them
    level.draw()
    # draw the rabbit if still alive
    if rabbit.alive:
        rabbit.draw()
    dog.draw()

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

    # the dog walks its route
    move_dog()

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


# moves the dog toward the next square in its route
def move_dog():
    # the pixel position of the center of the next square
    col, row = dog.route[dog.next_stop]
    target = level.map_to_pos(col, row)
    # the dog image faces right, so flip it when walking left
    if target[0] < dog.x:
        dog.flip_h = True
    elif target[0] > dog.x:
        dog.flip_h = False
    # move_toward() stops right on the target instead of going past it
    dog.move_toward(target, dog.velocity)
    # made it to that square, so head for the next one (back to the start at the end)
    if dog.pos == target:
        dog.next_stop += 1
        if dog.next_stop == len(dog.route):
            dog.next_stop = 0
    # the dog caught the rabbit, lose
    if dog.colliderect(rabbit):
        rabbit.alive = False
        game.lose()


pgzrun.go()
