# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from builder import build

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
player.pos = (WIDTH // 2, 0)
# define Actor-specific variables
player.alive = True
player.jumping = False
player.velocity_x = 3
player.velocity_y = 0

# global variables
jump_velocity = -10
gravity = 1

# build world
platforms = build("platformer_platforms.csv", 18)
obstacles = build("platformer_obstacles.csv", 18)


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
    # draw the player if still alive
    if player.alive:
        player.draw()


# updates game state between drawing of each frame
def update():
    # handle player left movement
    if keyboard.LEFT and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.image = "p_left"
        # if the movement caused a collision
        if player.collidelist(platforms) != -1:
            # get object that player collided with
            object = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.x = object.x + (object.width / 2 + player.width / 2)

    # handle player right movement
    elif keyboard.RIGHT and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.image = "p_right"
        # if the movement caused a collision
        if player.collidelist(platforms) != -1:
            # get object that player collided with
            object = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.x = object.x - (object.width / 2 + player.width / 2)

    # handle gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    # if the movement caused a collision, move position back
    if player.collidelist(platforms) != -1:
        # get object that player collided with
        object = platforms[player.collidelist(platforms)]
        # moving down - hit the ground
        if player.velocity_y >= 0:
            # move player up to no collision position
            player.y = object.y - (object.height / 2 + player.height / 2)
            # no longer jumping
            player.jumping = False
        # moving up - bumped their head
        else:
            # move player down to no collision position
            player.y = object.y + (object.height / 2 + player.height / 2)
        # reset velocity
        player.velocity_y = 0

    # player collided with obstacle, game over
    if player.collidelist(obstacles) != -1:
        player.alive = False


# keyboard pressed event listener
def on_key_down(key):
    # up key and not already jumping
    if key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True


pgzrun.go()  # program must always end with this
