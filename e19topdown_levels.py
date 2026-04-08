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
map_layers = load_tile_map_actors("tl1.tmx", scale=SCALE)
ground = map_layers["ground"]
walls = map_layers["walls"]
obstacles = map_layers["obstacles"]
hearts = map_layers["hearts"]

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
rabbit.pos = (200, HEIGHT / 2)
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
    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw()
    # draw hearts
    for heart in hearts:
        heart.draw()
    # draw the rabbit if still alive
    if rabbit.alive:
        rabbit.draw()

    # draw messages over top
    if game.state == "game_over":
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2))
    elif game.state == "win":
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))


# updates game state between drawing of each frame
def update():
    # if game state is not playing, just return
    if game.state != "playing":
        return

    # handle rabbit left movement
    if keyboard.LEFT:
        rabbit.x -= rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_left
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.left = collided.right

    # handle rabbit right movement
    elif keyboard.RIGHT:
        rabbit.x += rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_right
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.right = collided.left

    # handle rabbit up movement
    elif keyboard.UP:
        rabbit.y -= rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_up
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.top = collided.bottom

    # handle rabbit down movement
    elif keyboard.DOWN:
        rabbit.y += rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_down
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.bottom = collided.top

    # otherwise idle
    else:
        rabbit.sprite = idle

    # rabbit collided with obstacle, game over
    if rabbit.collidelist(obstacles) != -1:
        rabbit.alive = False
        game.state = "game_over"

    # check if rabbit collected hearts
    heart_index = rabbit.collidelist(hearts)
    if heart_index != -1:
        hearts.pop(heart_index)

    # check if rabbit collected all hearts
    if len(hearts) == 0:
        level_transition()


def level_transition():
    global ground, walls, obstacles, hearts
    # transition to level 2
    if game.level == 1 and (rabbit.left < 0 or rabbit.right > WIDTH or rabbit.top < 0 or rabbit.bottom > HEIGHT):
        # set level and new start position
        game.level = 2
        rabbit.pos = (0, rabbit.y)
        # build level 2 tile map
        map_layers = load_tile_map_actors("tl2.tmx", scale=SCALE)
        ground = map_layers["ground"]
        walls = map_layers["walls"]
        obstacles = map_layers["obstacles"]
        hearts = map_layers["hearts"]
    # transition to win
    elif game.level == 2:
        # set level and win
        game.level = 3
        game.state = "win"


pgzrun.go()  # program must always end with this
