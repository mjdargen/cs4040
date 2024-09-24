# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from platformer import *

# our platformer constants
TILE_SIZE = 18
ROWS = 30
COLS = 20

# Pygame constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Platformer"

# define Actor
player = Actor("p_right")
player.bottomleft = (0, HEIGHT)
# define Actor-specific variables
player.alive = True
player.jumping = False
player.velocity_x = 3
player.velocity_y = 0

# global variables
jump_velocity = -10
gravity = 1
win = False
over = False

# build world
platforms = build("platformer_platforms.csv", TILE_SIZE)
obstacles = build("platformer_obstacles.csv", TILE_SIZE)
mushrooms = build("platformer_mushrooms.csv", TILE_SIZE)


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
        if player.collidelist(platforms) != -1:
            # get object that player collided with
            collided = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.x = collided.x + (collided.width / 2 + player.width / 2)

    # handle player right movement
    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity_x
        player.image = "p_right"
        # if the movement caused a collision
        if player.collidelist(platforms) != -1:
            # get object that player collided with
            collided = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.x = collided.x - (collided.width / 2 + player.width / 2)

    # handle gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    # if the movement caused a collision, move position back
    if player.collidelist(platforms) != -1:
        # get object that player collided with
        collided = platforms[player.collidelist(platforms)]
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
    for mushroom in mushrooms:
        if player.colliderect(mushroom):
            mushrooms.remove(mushroom)

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
