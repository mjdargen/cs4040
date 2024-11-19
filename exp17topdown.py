import pgzrun  # program must always start with this
from pgone import *

# our tile map constants
TILE_SIZE = 18
ROWS = 30
COLS = 20
SCALE = 2

# Pygame constants
WIDTH = TILE_SIZE * ROWS * SCALE
HEIGHT = TILE_SIZE * COLS * SCALE
TITLE = "Top-Down Perspective"

# global variables
win = False
over = False

# build world from tile map
tilesheet = "levels/tilemap_packed.png"
ground = pgz_map("levels/topdown_ground.csv", tilesheet, TILE_SIZE, scale=SCALE)
walls = pgz_map("levels/topdown_walls.csv", tilesheet, TILE_SIZE, scale=SCALE)
obstacles = pgz_map("levels/topdown_obstacles.csv", tilesheet, TILE_SIZE, scale=SCALE)
hearts = pgz_map("levels/topdown_hearts.csv", tilesheet, TILE_SIZE, scale=SCALE)

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
rabbit.bottomleft = (WIDTH / 2, HEIGHT - TILE_SIZE)
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
    if over:
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2))
    if win:
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))


# updates game state between drawing of each frame
def update():
    # declare scope of global variables
    global win, over

    # if game is over, no more updating game state, just return
    if over or win:
        return

    # handle rabbit left movement
    if keyboard.LEFT and rabbit.left > 0:
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
    elif keyboard.RIGHT and rabbit.right < WIDTH:
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
    elif keyboard.UP and rabbit.top > 0:
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
    elif keyboard.DOWN and rabbit.bottom < HEIGHT:
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
        over = True

    # check if rabbit collected hearts
    heart_index = rabbit.collidelist(hearts)
    if heart_index != -1:
        hearts.pop(heart_index)

    # check if rabbit collected all hearts
    if len(hearts) == 0:
        win = True


pgzrun.go()  # program must always end with this
