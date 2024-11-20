import pgzrun
from pgzero.builtins import *
from pgone import *

# our tile map constants
TILE_SIZE = 18
ROWS = 30
COLS = 20
SCALE = 2

# Pygame constants
WIDTH = TILE_SIZE * ROWS * SCALE
HEIGHT = TILE_SIZE * COLS * SCALE
TITLE = "Platformer"


# global variables
jump_velocity = -15
gravity = 1
win = False
over = False
level = 1

# build world
# import in tile map
tilesheet = "levels/tilemap_packed.png"
platforms = pgz_map("levels/p1_platforms.csv", tilesheet, TILE_SIZE, scale=SCALE)
obstacles = pgz_map("levels/p1_obstacles.csv", tilesheet, TILE_SIZE, scale=SCALE)
mushrooms = pgz_map("levels/p1_mushrooms.csv", tilesheet, TILE_SIZE, scale=SCALE)


# define Sprites
filename = "fox.png"  # Name of file, must be stored in "images" folder
frame_width = 24  # width of each frame
frame_height = 16  # height of each frame
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
fox_stand = Sprite(filename, frame_width, frame_height, 1, 14, 2)
fox_walk = Sprite(filename, frame_width, frame_height, 2, 8, 10)

# define SpriteActor
fox = SpriteActor(fox_stand)
fox.scale = 2.5
fox.bottomleft = (0, HEIGHT-40)
# define Actor-specific variables
fox.alive = True
fox.jumping = False
fox.velocity_x = 5
fox.velocity_y = 0


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color
    # draw platforms
    for platform in platforms:
        platform.draw()
    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw()
    # draw mushrooms
    for mushroom in mushrooms:
        mushroom.draw()
    # draw the fox if still alive
    if fox.alive:
        fox.draw()

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

    # handle fox left movement
    if keyboard.LEFT and fox.left > 0:
        fox.x -= fox.velocity_x
        # flip image and change sprite
        fox.sprite = fox_walk
        fox.flip_h = True
        # if the movement caused a collision
        collision_index = fox.collidelist(platforms)
        if collision_index != -1:
            # get object that fox collided with
            collided = platforms[collision_index]
            # use it to calculate position where there is no collision
            fox.left = collided.right

    # handle fox right movement
    elif keyboard.RIGHT and fox.right < WIDTH:
        fox.x += fox.velocity_x
        # flip image and change sprite
        fox.sprite = fox_walk
        fox.flip_h = False
        # if the movement caused a collision
        collision_index = fox.collidelist(platforms)
        if collision_index != -1:
            # get object that fox collided with
            collided = platforms[collision_index]
            # use it to calculate position where there is no collision
            fox.right = collided.left

    # handle gravity
    fox.y += fox.velocity_y
    fox.velocity_y += gravity
    # if the movement caused a collision, move position back
    collision_index = fox.collidelist(platforms)
    if collision_index != -1:
        # get object that fox collided with
        collided = platforms[collision_index]
        # moving down - hit the ground
        if fox.velocity_y >= 0:
            # move fox up to no collision position
            fox.bottom = collided.top
            # no longer jumping
            fox.jumping = False
        # moving up - bumped their head
        else:
            # move fox down to no collision position
            fox.top = collided.bottom
        # reset velocity
        fox.velocity_y = 0

    # fox collided with obstacle, game over
    if fox.collidelist(obstacles) != -1:
        fox.alive = False
        over = True

    # check if fox collected mushrooms
    if fox.collidelist(mushrooms) != -1:
        mushroom_index = fox.collidelist(mushrooms)
        mushrooms.pop(mushroom_index)

    # check if fox collected all mushrooms
    if len(mushrooms) == 0:
        level_transition()


def level_transition():
    global level, win, platforms, obstacles, mushrooms
    # transition to level 2
    if level == 1:
        # set level and new start position
        level = 2
        fox.bottomleft = (0, HEIGHT-40)
        # import new tilemap to pgzero
        platforms = pgz_map("levels/p2_platforms.csv", tilesheet, TILE_SIZE, scale=SCALE)
        obstacles = pgz_map("levels/p2_obstacles.csv", tilesheet, TILE_SIZE, scale=SCALE)
        mushrooms = pgz_map("levels/p2_mushrooms.csv", tilesheet, TILE_SIZE, scale=SCALE)
    # transition to win
    elif level == 2:
        # set level and win
        level = 3
        win = True


# keyboard pressed event listener
def on_key_down(key):
    # up key and not already jumping
    if key == keys.UP and not fox.jumping:
        fox.velocity_y = jump_velocity
        fox.jumping = True


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        fox.sprite = fox_stand


pgzrun.go()  # program must always end with this
