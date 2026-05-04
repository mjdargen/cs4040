import pgzrun
from pgzero.builtins import *

# our tile map constants
TILE_SIZE = 18
ROWS = 30
COLS = 20
SCALE = 2
WORLD_WIDTH = 90
WORLD_HEIGHT = 60

# Pygame Constants
WIDTH = TILE_SIZE * ROWS * SCALE
HEIGHT = TILE_SIZE * COLS * SCALE
TITLE = "Top-Down Perspective"

# build world from Tiled tile map
map_layers = load_tile_map_actors("topdown_open_world.tmx", scale=SCALE)
ground = map_layers["ground"]
walls = map_layers["walls"]
hazards = map_layers["hazards"]
collectables = map_layers["collectables"]
# add entire tile map to a single list just for player "movement"
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
# define Actor-specific variables
rabbit.alive = True
rabbit.jumping = False
rabbit.velocity = 5


# runs once at beginning before draw()/update()
def start():
    # player should start in the middle of the world
    # to do so, we need to shift the whole world so middle of world = middle of screen
    for tile in world:
        tile.x -= WORLD_WIDTH / 2 * TILE_SIZE * SCALE
        tile.y -= WORLD_HEIGHT / 2 * TILE_SIZE * SCALE
    # place payer in the middle of screen
    rabbit.pos = (WIDTH / 2, HEIGHT / 2)


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
        # change sprite based on direction
        rabbit.sprite = walk_left
        # change position of player temporarily to check for collision
        rabbit.x -= rabbit.velocity
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        # if we did not collide with a wall
        if collision_index == -1:
            # move the world instead of player in opposite direction
            for tile in world:
                tile.x += rabbit.velocity
        # always move player back
        rabbit.x += rabbit.velocity

    # handle rabbit right movement
    elif keyboard.RIGHT:
        # change sprite based on direction
        rabbit.sprite = walk_right
        # change position of player temporarily to check for collision
        rabbit.x += rabbit.velocity
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        # if we did not collide with a wall
        if collision_index == -1:
            # move the world instead of player in opposite direction
            for tile in world:
                tile.x -= rabbit.velocity
        # always move player back
        rabbit.x -= rabbit.velocity

    # handle rabbit up movement
    elif keyboard.UP:
        # change sprite based on direction
        rabbit.sprite = walk_up
        # change position of player temporarily to check for collision
        rabbit.y -= rabbit.velocity
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        # if we did not collide with a wall
        if collision_index == -1:
            # move the world instead of player in opposite direction
            for tile in world:
                tile.y += rabbit.velocity
        # always move player back
        rabbit.y += rabbit.velocity

    # handle rabbit down movement
    elif keyboard.DOWN:
        # change sprite based on direction
        rabbit.sprite = walk_down
        # change position of player temporarily to check for collision
        rabbit.y += rabbit.velocity
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        # if we did not collide with a wall
        if collision_index == -1:
            # move the world instead of player in opposite direction
            for tile in world:
                tile.y -= rabbit.velocity
        # always move player back
        rabbit.y -= rabbit.velocity

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
