import pgzrun
from pgzero.builtins import *

# our tile map constants
TILE_SIZE = 18
MAP_WIDTH = 30
MAP_HEIGHT = 20
SCALE = 2

# Pygame Constants
WIDTH = TILE_SIZE * MAP_WIDTH * SCALE
HEIGHT = TILE_SIZE * MAP_HEIGHT * SCALE
TITLE = "Platformer"


# global variables
gravity = 1

# build world from Tiled tile map
map_layers = load_tile_map_actors("pl1.tmx", scale=SCALE)
platforms = map_layers["platforms"]
hazards = map_layers["hazards"]
collectables = map_layers["collectables"]

# define Sprites
filename = "fox.png"  # Name of file, must be stored in "images" folder
frame_width = 24  # width of each frame
frame_height = 16  # height of each frame
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
fox_idle = Sprite(filename, frame_width, frame_height, 1, 14, 2)
fox_walk = Sprite(filename, frame_width, frame_height, 2, 8, 10)

# define SpriteActor
fox = SpriteActor(fox_idle)
fox.scale = 2.5
fox.bottomleft = (0, HEIGHT - 40)
# define Actor-specific variables
fox.alive = True
fox.on_ground = False
fox.velocity_x = 5
fox.velocity_y = 0
fox.jump_velocity = -16


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color
    # draw platforms
    for platform in platforms:
        platform.draw()
    # draw hazards
    for hazard in hazards:
        hazard.draw()
    # draw collectables
    for mushroom in collectables:
        mushroom.draw()
    # draw the fox if still alive
    if fox.alive:
        fox.draw()

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
            collided_platform = platforms[collision_index]
            # use it to calculate position where there is no collision
            fox.left = collided_platform.right

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
            collided_platform = platforms[collision_index]
            # use it to calculate position where there is no collision
            fox.right = collided_platform.left

    # apply gravity
    fox.velocity_y += gravity
    # assume not on the ground unless a collision proves otherwise
    fox.on_ground = False
    # move vertically
    fox.y += fox.velocity_y
    # check for platform collision
    collision_index = fox.collidelist(platforms)
    if collision_index != -1:
        # get the platform that cause the collision
        collided_platform = platforms[collision_index]
        # falling down - landed on top of a platform
        if fox.velocity_y > 0:
            fox.bottom = collided_platform.top
            fox.on_ground = True
        # moving up - bumped head on bottom of a platform
        elif fox.velocity_y < 0:
            fox.top = collided_platform.bottom
        # stop vertical movement after hitting something
        fox.velocity_y = 0

    # fox collided with hazard, game over
    if fox.collidelist(hazards) != -1:
        fox.alive = False
        game.lose()

    # check if fox collected collectables
    if fox.collidelist(collectables) != -1:
        mushroom_index = fox.collidelist(collectables)
        collectables.pop(mushroom_index)

    # check if fox collected all collectables
    if len(collectables) == 0:
        level_transition()


def level_transition():
    global platforms, hazards, collectables
    # transition to level 2
    if game.level == 1:
        # set level and new start position
        game.level = 2
        fox.bottomleft = (0, HEIGHT - 40)
        # build level 2 tile map
        map_layers = load_tile_map_actors("pl2.tmx", scale=SCALE)
        platforms = map_layers["platforms"]
        hazards = map_layers["hazards"]
        collectables = map_layers["collectables"]
    # transition to win
    elif game.level == 2:
        # set level and win
        game.level = 3
        game.win()


# keyboard pressed event listener
def on_key_down(key):
    # up key and on the ground
    if key == keys.UP and fox.on_ground:
        fox.velocity_y = fox.jump_velocity


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        fox.sprite = fox_idle


pgzrun.go()  # program must always end with this
