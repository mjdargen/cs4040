import pgzrun
from pgzero.builtins import *

# tile map scale
MAP_SCALE = 2

# load world from Tiled tile map
level = load_tile_map("platformer_moving_platforms.tmx", scale=MAP_SCALE)
platforms = level["platforms"]
moving = level["moving"]  # platforms that slide back and forth
hazards = level["hazards"]
collectables = level["collectables"]

# Pygame Constants - compute with level dimensions
WIDTH = level.cols * level.tile_width
HEIGHT = level.rows * level.tile_height
TITLE = "Platformer with Moving Platforms"

# define Sprites
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=2)
fox_walk = Sprite("fox", frame_width=24, frame_height=16, row=2, frames=8, fps=10)

# define the Actor
fox = Actor(fox_idle)

# global variables
gravity = 1
# All the tiles in the moving layer move together, in the same direction.
# To have platforms that move separately, put them on another layer (like "moving2")
# with its own speed and distance variables, and move it the same way.
platform_speed = 2  # pixels the moving platforms move each frame (negative is left)
platform_distance = 0  # how far the moving platforms are from where they started


# runs once at beginning before draw()/update()
def start():
    fox.scale = 2.5
    fox.bottomleft = (0, HEIGHT - 40)
    fox.alive = True
    fox.on_ground = False
    fox.on_moving_platform = False
    fox.velocity_x = 5
    fox.velocity_y = 0
    fox.jump_velocity = -16


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color
    # draw every layer of the tile map, in the order Tiled shows them
    level.draw()
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

    # move the moving platforms first, so the fox can ride along with them
    move_platforms()

    # handle left movement
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

    # handle right movement
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
    # otherwise idle
    else:
        fox.sprite = fox_idle

    # assume not on the ground unless a collision proves otherwise
    fox.on_ground = False
    fox.on_moving_platform = False
    # apply gravity
    fox.velocity_y += gravity
    # move vertically
    fox.y += fox.velocity_y
    # check for platform collision
    collision_index = fox.collidelist(platforms)
    if collision_index != -1:
        # get the platform that caused the collision
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

    # check for moving platform collision, the same way
    collision_index = fox.collidelist(moving)
    if collision_index != -1:
        # get the moving platform that caused the collision
        collided_platform = moving[collision_index]
        # falling down - landed on top of a moving platform
        if fox.velocity_y > 0:
            fox.bottom = collided_platform.top
            fox.on_ground = True
            fox.on_moving_platform = True  # ride along with it next frame
        # moving up - bumped head on bottom of a moving platform
        elif fox.velocity_y < 0:
            fox.top = collided_platform.bottom
        # stop vertical movement after hitting something
        fox.velocity_y = 0

    # fox collided with hazard, lose
    if fox.collidelist(hazards) != -1:
        fox.alive = False
        game.lose()

    # check if fox collected collectables
    mushroom_index = fox.collidelist(collectables)
    if mushroom_index != -1:
        collectables.pop(mushroom_index)

    # check if fox collected all collectables
    if len(collectables) == 0:
        game.win()


# moves the moving platforms back and forth, carrying the fox if it's standing on one
def move_platforms():
    global platform_speed, platform_distance
    # move every tile in the moving layer
    for tile in moving:
        tile.x += platform_speed
    # if the fox is standing on a moving platform, move it the same amount
    if fox.on_moving_platform:
        fox.x += platform_speed
    # keep track of how far the platforms are from where they started
    platform_distance += platform_speed
    # turn around after moving 144 pixels (4 tiles) away, or when back at the start
    if platform_distance >= 144 or platform_distance <= 0:
        platform_speed = -platform_speed


# keyboard pressed event listener
def on_key_down(key):
    # up key and on the ground
    if key == keys.UP and fox.on_ground:
        fox.velocity_y = fox.jump_velocity


pgzrun.go()
