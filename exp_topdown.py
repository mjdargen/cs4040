import pgzrun
from pgzero.builtins import *

# our tile map constants
TILE_SIZE = 18
ROWS = 30
COLS = 20
SCALE = 2

# Pygame Constants
WIDTH = TILE_SIZE * ROWS * SCALE
HEIGHT = TILE_SIZE * COLS * SCALE
TITLE = "Top-Down Perspective"

# build world from Tiled tile map
map_layers = load_tile_map_actors("topdown.tmx", scale=SCALE)
ground = map_layers["ground"]
walls = map_layers["walls"]
hazards = map_layers["hazards"]
collectables = map_layers["collectables"]
world = []
world.extend(ground)
world.extend(walls)
world.extend(hazards)
world.extend(collectables)

# define Sprites
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
filename = "rabbit.png"
frame_width = 16  # width of each frame
frame_height = 16  # height of each frame
idle = Sprite(filename, frame_width, frame_height, 0, 2, 3)
walk_down = Sprite(filename, frame_width, frame_height, 4, 4, 10)
walk_up = Sprite(filename, frame_width, frame_height, 5, 4, 10)
walk_left = Sprite(filename, frame_width, frame_height, 6, 4, 10)
walk_right = Sprite(filename, frame_width, frame_height, 7, 4, 10)

# define SpriteActor
rabbit = SpriteActor(idle)
rabbit.scale = SCALE
rabbit.pos = (WIDTH / 2, HEIGHT - TILE_SIZE)
# define Actor-specific variables
rabbit.alive = True
rabbit.jumping = False
rabbit.velocity = 4


# displays the new frame
def draw():
    screen.clear()  # clears the screen

    # draw ground
    for tile in ground:
        tile.draw()
    # draw walls
    for wall in walls:
        wall.draw()
    # draw hazards
    for hazard in hazards:
        hazard.draw()
    # draw collectables
    for heart in collectables:
        heart.draw()
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
        # rabbit.x -= rabbit.velocity
        for tile in world:
            tile.x += rabbit.velocity
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
        # rabbit.x += rabbit.velocity
        rabbit.sprite = walk_right
        for tile in world:
            tile.x -= rabbit.velocity
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

    # rabbit collided with hazard, game over
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
