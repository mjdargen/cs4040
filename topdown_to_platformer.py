import pgzrun
from pgzero.builtins import *

# tile map scale
MAP_SCALE = 2

# load world from Tiled tile map (level 1 is top-down)
level = load_tile_map("tl1.tmx", scale=MAP_SCALE)
ground = level["ground"]
walls = level["walls"]
hazards = level["hazards"]
collectables = level["collectables"]
# level 2 is a platformer, so its platforms are loaded in level_transition()
platforms = []

# Pygame Constants - compute with level dimensions
WIDTH = level.cols * level.tile_width
HEIGHT = level.rows * level.tile_height
TITLE = "Top-Down to Platformer"

# define Sprites
idle = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=3)
walk_down = Sprite("rabbit", frame_width=16, frame_height=16, row=4, frames=2, fps=10)
walk_up = Sprite("rabbit", frame_width=16, frame_height=16, row=5, frames=2, fps=10)
walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=2, fps=10)
walk_right = Sprite("rabbit", frame_width=16, frame_height=16, row=7, frames=2, fps=10)

# define the Actor
rabbit = Actor(idle)

# global variables
gravity = 1


# runs once at beginning before draw()/update()
def start():
    rabbit.scale = MAP_SCALE
    rabbit.pos = (200, HEIGHT / 2)
    rabbit.alive = True
    # top-down movement (level 1)
    rabbit.velocity = 4
    # platformer movement (level 2)
    rabbit.on_ground = False
    rabbit.velocity_x = 5
    rabbit.velocity_y = 0
    rabbit.jump_velocity = -16


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    # the platformer level has a sky color behind its tiles
    if game.level == 2:
        screen.fill("lightslateblue")  # fills background color
    # draw every layer of the tile map, in the order Tiled shows them
    level.draw()
    # draw the rabbit if still alive
    if rabbit.alive:
        rabbit.draw()

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

    # move using the controls for the current level
    if game.level == 1:
        topdown_movement()
    elif game.level == 2:
        platformer_movement()

    # rabbit collided with hazard, lose
    if rabbit.collidelist(hazards) != -1:
        rabbit.alive = False
        game.lose()

    # check if rabbit collected collectables
    item_index = rabbit.collidelist(collectables)
    if item_index != -1:
        collectables.pop(item_index)

    # check if rabbit collected all collectables
    if len(collectables) == 0:
        level_transition()


# top-down movement: four directions, no gravity
def topdown_movement():
    # handle rabbit left movement
    if keyboard.LEFT:
        # change x position and sprite
        rabbit.x -= rabbit.velocity
        rabbit.sprite = walk_left
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.left = collided_wall.right

    # handle rabbit right movement
    elif keyboard.RIGHT:
        # change x position and sprite
        rabbit.x += rabbit.velocity
        rabbit.sprite = walk_right
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.right = collided_wall.left

    # handle rabbit up movement
    elif keyboard.UP:
        # change y position and sprite
        rabbit.y -= rabbit.velocity
        rabbit.sprite = walk_up
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.top = collided_wall.bottom

    # handle rabbit down movement
    elif keyboard.DOWN:
        # change y position and sprite
        rabbit.y += rabbit.velocity
        rabbit.sprite = walk_down
        # if the movement caused a collision
        collision_index = rabbit.collidelist(walls)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_wall = walls[collision_index]
            # use it to calculate position where there is no collision
            rabbit.bottom = collided_wall.top

    # otherwise idle
    else:
        rabbit.sprite = idle


# platformer movement: left and right with gravity (jumping is in on_key_down)
def platformer_movement():
    # handle left movement
    if keyboard.LEFT and rabbit.left > 0:
        rabbit.x -= rabbit.velocity_x
        rabbit.sprite = walk_left
        # if the movement caused a collision
        collision_index = rabbit.collidelist(platforms)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_platform = platforms[collision_index]
            # use it to calculate position where there is no collision
            rabbit.left = collided_platform.right

    # handle right movement
    elif keyboard.RIGHT and rabbit.right < WIDTH:
        rabbit.x += rabbit.velocity_x
        rabbit.sprite = walk_right
        # if the movement caused a collision
        collision_index = rabbit.collidelist(platforms)
        if collision_index != -1:
            # get object that rabbit collided with
            collided_platform = platforms[collision_index]
            # use it to calculate position where there is no collision
            rabbit.right = collided_platform.left
    # otherwise idle
    else:
        rabbit.sprite = idle

    # assume not on the ground unless a collision proves otherwise
    rabbit.on_ground = False
    # apply gravity
    rabbit.velocity_y += gravity
    # move vertically
    rabbit.y += rabbit.velocity_y
    # check for platform collision
    collision_index = rabbit.collidelist(platforms)
    if collision_index != -1:
        # get the platform that caused the collision
        collided_platform = platforms[collision_index]
        # falling down - landed on top of a platform
        if rabbit.velocity_y > 0:
            rabbit.bottom = collided_platform.top
            rabbit.on_ground = True
        # moving up - bumped head on bottom of a platform
        elif rabbit.velocity_y < 0:
            rabbit.top = collided_platform.bottom
        # stop vertical movement after hitting something
        rabbit.velocity_y = 0


def level_transition():
    global level, platforms, hazards, collectables
    # transition to level 2 once the rabbit walks off the screen
    if game.level == 1 and (rabbit.left < 0 or rabbit.right > WIDTH or rabbit.top < 0 or rabbit.bottom > HEIGHT):
        # set level
        game.level = 2
        # build level 2 tile map. Its tiles are 18 pixels instead of 16, so
        # scale them down to the same size on screen to fit the same window
        level = load_tile_map("pl1.tmx", scale=MAP_SCALE * 16 / 18)
        platforms = level["platforms"]
        hazards = level["hazards"]
        collectables = level["collectables"]
        # new start position in the bottom left corner, not falling yet
        rabbit.bottomleft = (0, HEIGHT - 40)
        rabbit.velocity_y = 0
    # transition to win
    elif game.level == 2:
        # signal win and set idle
        game.win()
        rabbit.sprite = idle


# keyboard pressed event listener
def on_key_down(key):
    # up key and on the ground, only in the platformer level
    if key == keys.UP and game.level == 2 and rabbit.on_ground:
        rabbit.velocity_y = rabbit.jump_velocity


pgzrun.go()
