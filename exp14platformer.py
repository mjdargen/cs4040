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

# define Actor
player = Actor("p_right")
player.scale = SCALE
player.bottomleft = (0, HEIGHT)
# define Actor-specific variables
player.alive = True
player.jumping = False
player.velocity_x = 5
player.velocity_y = 0

# global variables
jump_velocity = -15
gravity = 1
win = False
over = False

# build world from
tilesheet = "levels/tilemap_packed.png"
platforms = pgz_map("levels/platformer_platforms.csv", tilesheet, TILE_SIZE, scale=SCALE)
obstacles = pgz_map("levels/platformer_obstacles.csv", tilesheet, TILE_SIZE, scale=SCALE)
mushrooms = pgz_map("levels/platformer_mushrooms.csv", tilesheet, TILE_SIZE, scale=SCALE)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color
    if over:
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2))
    if win:
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))
    # draw platforms
    for platform in platforms:
        platform.draw()
    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw()
    # draw mushrooms
    for mushroom in mushrooms:
        mushroom.draw()
    # draw the player if still alive
    if player.alive:
        player.draw()


# updates game state between drawing of each frame
def update():
    # declare scope of global variables
    global win, over

    # if game is over, no more updating game state, just return
    if over or win:
        return

    # handle player left movement
    if keyboard.LEFT and player.left > 0:
        player.x -= player.velocity_x
        player.image = "p_left"
        # if the movement caused a collision
        collision_index = player.collidelist(platforms)
        if collision_index != -1:
            # get object that player collided with
            collided = platforms[collision_index]
            # use it to calculate position where there is no collision
            player.left = collided.right

    # handle player right movement
    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity_x
        player.image = "p_right"
        # if the movement caused a collision
        collision_index = player.collidelist(platforms)
        if collision_index != -1:
            # get object that player collided with
            collided = platforms[collision_index]
            # use it to calculate position where there is no collision
            player.right = collided.left

    # handle gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    # if the movement caused a collision, move position back
    collision_index = player.collidelist(platforms)
    if collision_index != -1:
        # get object that player collided with
        collided = platforms[collision_index]
        # moving down - hit the ground
        if player.velocity_y >= 0:
            # move player up to no collision position
            player.bottom = collided.top
            # no longer jumping
            player.jumping = False
        # moving up - bumped their head
        else:
            # move player down to no collision position
            player.top = collided.bottom
        # reset velocity
        player.velocity_y = 0

    # player collided with obstacle, game over
    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True

    # check if player collected mushrooms
    if player.collidelist(mushrooms) != -1:
        mushroom_index = player.collidelist(mushrooms)
        mushrooms.pop(mushroom_index)

    # check if player collected all mushrooms
    if len(mushrooms) == 0:
        win = True


# keyboard pressed event listener
def on_key_down(key):
    # up key and not already jumping
    if key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True


pgzrun.go()  # program must always end with this
