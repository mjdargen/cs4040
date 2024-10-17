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


# global variables
jump_velocity = -10
gravity = 1
win = False
over = False

# build world
platforms = build("platformer_files/platformer_platforms.csv", TILE_SIZE)
obstacles = build("platformer_files/platformer_obstacles.csv", TILE_SIZE)
mushrooms = build("platformer_files/platformer_mushrooms.csv", TILE_SIZE)

# define Sprites
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
color_key = (0, 0, 0)  # leave like this unless background shows up
fox_stand = Sprite("fox.png", (0, 16, 24, 16), 14, color_key, 30)
fox_walk = Sprite("fox.png", (0, 2 * 16, 24, 16), 8, color_key, 5)

# define SpriteActor
fox = SpriteActor(fox_stand)
fox.bottomleft = (0, HEIGHT)
# define Actor-specific variables
fox.alive = True
fox.jumping = False
fox.velocity_x = 3
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
        if fox.collidelist(platforms) != -1:
            # get object that fox collided with
            collided = platforms[fox.collidelist(platforms)]
            # use it to calculate position where there is no collision
            fox.left = collided.right

    # handle fox right movement
    elif keyboard.RIGHT and fox.right < WIDTH:
        fox.x += fox.velocity_x
        # flip image and change sprite
        fox.sprite = fox_walk
        fox.flip_h = False
        # if the movement caused a collision
        if fox.collidelist(platforms) != -1:
            # get object that fox collided with
            collided = platforms[fox.collidelist(platforms)]
            # use it to calculate position where there is no collision
            fox.right = collided.left

    # handle gravity
    fox.y += fox.velocity_y
    fox.velocity_y += gravity
    # if the movement caused a collision, move position back
    if fox.collidelist(platforms) != -1:
        # get object that fox collided with
        collided = platforms[fox.collidelist(platforms)]
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
    for mushroom in mushrooms:
        if fox.colliderect(mushroom):
            mushrooms.remove(mushroom)

    # check if fox collected all mushrooms
    if len(mushrooms) == 0:
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
