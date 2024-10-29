import pgzrun  # program must always start with this
from platformer import *

# our platformer constants
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

# build world
ground = build("top_down_files/topdown_ground.csv", TILE_SIZE, SCALE)
walls = build("top_down_files/topdown_walls.csv", TILE_SIZE, SCALE)
obstacles = build("top_down_files/topdown_obstacles.csv", TILE_SIZE, SCALE)
hearts = build("top_down_files/topdown_hearts.csv", TILE_SIZE, SCALE)

# define Sprites
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
color_key = (0, 0, 0)  # leave like this unless background shows up
idle = Sprite("rabbit.png", (0, 0, 16, 16), 2, color_key, 30)
walk_down = Sprite("rabbit.png", (0, 4 * 16, 16, 16), 2, color_key, 10)
walk_up = Sprite("rabbit.png", (0, 5 * 16, 16, 16), 2, color_key, 10)
walk_left = Sprite("rabbit.png", (0, 6 * 16, 16, 16), 2, color_key, 10)
walk_right = Sprite("rabbit.png", (0, 7 * 16, 16, 16), 2, color_key, 10)

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
    screen.fill("lightslateblue")  # fills background color

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
        if rabbit.collidelist(walls) != -1:
            # get object that rabbit collided with
            collided = walls[rabbit.collidelist(walls)]
            # use it to calculate position where there is no collision
            rabbit.left = collided.right

    # handle rabbit right movement
    elif keyboard.RIGHT and rabbit.right < WIDTH:
        rabbit.x += rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_right
        # if the movement caused a collision
        if rabbit.collidelist(walls) != -1:
            # get object that rabbit collided with
            collided = walls[rabbit.collidelist(walls)]
            # use it to calculate position where there is no collision
            rabbit.right = collided.left

    # handle rabbit up movement
    elif keyboard.UP and rabbit.top > 0:
        rabbit.y -= rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_up
        # if the movement caused a collision
        if rabbit.collidelist(walls) != -1:
            # get object that rabbit collided with
            collided = walls[rabbit.collidelist(walls)]
            # use it to calculate position where there is no collision
            rabbit.top = collided.bottom

    # handle rabbit down movement
    elif keyboard.DOWN and rabbit.bottom < HEIGHT:
        rabbit.y += rabbit.velocity
        # flip image and change x velocity
        rabbit.sprite = walk_down
        # if the movement caused a collision
        if rabbit.collidelist(walls) != -1:
            # get object that rabbit collided with
            collided = walls[rabbit.collidelist(walls)]
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
    if rabbit.collidelist(hearts) != -1:
        heart_index = rabbit.collidelist(hearts)
        hearts.pop(heart_index)

    # check if rabbit collected all hearts
    if len(hearts) == 0:
        win = True


pgzrun.go()  # program must always end with this
