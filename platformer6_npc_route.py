import pgzrun
from pgzero.builtins import *

# tile map scale
MAP_SCALE = 2

# load world from Tiled tile map
level = load_tile_map("platformer.tmx", scale=MAP_SCALE)
platforms = level["platforms"]
hazards = level["hazards"]
collectables = level["collectables"]

# Pygame Constants - compute with level dimensions
WIDTH = level.cols * level.tile_width
HEIGHT = level.rows * level.tile_height
TITLE = "Platformer NPC Route"

# define Sprites
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=2)
fox_walk = Sprite("fox", frame_width=24, frame_height=16, row=2, frames=8, fps=10)
bee_fly = Sprite(["bee_a", "bee_b"], fps=8)

# define the Actors
fox = Actor(fox_idle)
bee = Actor(bee_fly)  # an NPC (non-player character) that flies around on its own

# global variables
gravity = 1


# runs once at beginning before draw()/update()
def start():
    fox.scale = 2.5
    fox.bottomleft = (0, HEIGHT - 40)
    fox.alive = True
    fox.on_ground = False
    fox.velocity_x = 5
    fox.velocity_y = 0
    fox.jump_velocity = -16
    bee.scale = 0.5
    bee.velocity = 2
    # the bee's route: the squares where it turns, as (column, row),
    # found by hovering over the map in Tiled. It flies back and forth
    # through the open air in the middle, where nothing else is.
    bee.route = [(4, 10), (22, 10)]
    bee.next_stop = 0  # index of the square in the route it's flying to
    # start the bee on the first square of its route
    col, row = bee.route[0]
    bee.pos = level.map_to_pos(col, row)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color
    # draw every layer of the tile map, in the order Tiled shows them
    level.draw()
    # draw the fox if still alive
    if fox.alive:
        fox.draw()
    bee.draw()

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

    # the bee flies its route
    move_bee()

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


# moves the bee toward the next square in its route
def move_bee():
    # the pixel position of the center of the next square
    col, row = bee.route[bee.next_stop]
    target = level.map_to_pos(col, row)
    # the bee images face left, so flip them when the bee flies right
    if target[0] > bee.x:
        bee.flip_h = True
    elif target[0] < bee.x:
        bee.flip_h = False
    # move_toward() stops right on the target instead of going past it
    bee.move_toward(target, bee.velocity)
    # made it to that square, so head for the next one (back to the start at the end)
    if bee.pos == target:
        bee.next_stop += 1
        if bee.next_stop == len(bee.route):
            bee.next_stop = 0
    # the bee caught the fox, lose
    if bee.colliderect(fox):
        fox.alive = False
        game.lose()


# keyboard pressed event listener
def on_key_down(key):
    # up key and on the ground
    if key == keys.UP and fox.on_ground:
        fox.velocity_y = fox.jump_velocity


pgzrun.go()
