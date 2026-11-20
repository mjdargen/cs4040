import pgzrun
from pgzero.builtins import *

# tile map scale
MAP_SCALE = 0.75  # 64 * 0.75 = 48 pixel tiles on the screen

# load world from Tiled tile map
level = load_tile_map("platformer_slopes.tmx", scale=MAP_SCALE)
platforms = level["platforms"]
# each slope tile has two custom properties set in Tiled:
#   left_height  - how high the ground is at the left edge of the tile
#   right_height - how high the ground is at the right edge of the tile
# both are measured up from the bottom of the tile, in tileset pixels (0 to 64)
slopes = level["slopes"]

# Pygame Constants - compute with level dimensions
WIDTH = level.cols * level.tile_width
HEIGHT = level.rows * level.tile_height
TITLE = "Platformer Slopes"

# define Sprites
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=0, frames=5, fps=5)
fox_walk = Sprite("fox", frame_width=24, frame_height=16, row=2, frames=8, fps=10)

# define the Actor
fox = Actor(fox_idle)

# global variables
gravity = 1
# the tallest ledge the fox can walk up without jumping, in pixels
# (where a slope meets a block, the fox's feet end up a little below the block)
STEP_UP_HEIGHT = 16
show_slope_lines = False


# runs once at beginning before draw()/update()
def start():
    fox.scale = 2
    # a narrow body, so the fox stands on a slope by the middle of its feet
    fox.collision_rect = (12, 16)
    fox.pos = level.map_to_pos(0, 7)  # just above the ground at the left
    fox.on_ground = False
    fox.velocity_x = 5
    fox.velocity_y = 0
    fox.jump_velocity = -16


# finds the y of the ground on a slope tile at a given x
# the ground on a slope is a straight line, so we can use rise over run
def ground_y_on_slope(tile, x):
    # height of the ground at each edge, converted to screen pixels
    left_height = tile.properties["left_height"] * MAP_SCALE
    right_height = tile.properties["right_height"] * MAP_SCALE
    # a tile flipped in Tiled slopes the other way, so swap the edges
    if tile.flip_h:
        left_height, right_height = right_height, left_height

    # slope = rise / run
    # rise: how much the ground goes up from the left edge to the right edge
    # run: how far it is from the left edge to the right edge
    rise = right_height - left_height
    run = tile.width
    slope = rise / run

    # how far x is from the left edge of the tile (kept inside the tile)
    distance = x - tile.left
    if distance < 0:
        distance = 0
    if distance > run:
        distance = run

    # like y = mx + b: start at the left edge's height (b),
    # then go up by slope (m) for every pixel we move right (x)
    height = left_height + slope * distance

    # screen y counts DOWN from the top, so a taller ground means a smaller y
    return tile.bottom - height


# finds the slope tile under the fox's feet, or None if there isn't one
def find_slope_under_fox():
    column, row = level.pos_to_map(fox.x, fox.bottom)
    # check the tile at the fox's feet, the one above it (gravity may have
    # pulled the feet just past the slope) and the one below (walking downhill)
    for check_row in [row - 1, row, row + 1]:
        tile = slopes.get_tile(column, check_row)
        if tile is not None:
            return tile
    return None


# puts the fox's feet on the slope under it, if there is one
def land_on_slope(was_on_ground):
    slope_tile = find_slope_under_fox()
    if slope_tile is None:
        return

    # fox.x is the middle of the fox, so it stands by the middle of its feet
    ground_y = ground_y_on_slope(slope_tile, fox.x)

    # walking downhill, the ground drops away under the fox each frame
    # the steepest slope has rise / run = 1, so walking velocity_x pixels
    # sideways can drop the ground velocity_x pixels too
    # if the fox was already on the ground, let it reach down that far
    # (plus a little extra) so it sticks to the slope instead of falling
    if was_on_ground:
        reach_down = fox.velocity_x + STEP_UP_HEIGHT
    else:
        reach_down = 0

    # not jumping up, and the feet are at (or close enough to) the ground
    if fox.velocity_y >= 0 and fox.bottom + reach_down >= ground_y:
        fox.bottom = ground_y
        fox.on_ground = True


# tries to step the fox up onto a short ledge it walked into
# returns True if it stepped up, False if the platform is a wall
def try_step_up(platform):
    ledge_height = fox.bottom - platform.top
    if fox.on_ground and 0 < ledge_height <= STEP_UP_HEIGHT:
        # lift the fox up onto the ledge
        fox.bottom = platform.top
        # nothing in the way now, so it was a short ledge
        if fox.collidelist(platforms) == -1:
            return True
        # still blocked, so it's a wall: put the fox back down
        fox.bottom += ledge_height
    return False


# displays the new frame
def draw():
    screen.clear()
    screen.fill("lightblue")
    level.draw()
    fox.draw()
    # draw the line each slope tile's ground follows
    if show_slope_lines:
        fox.draw_collision_rect()
        for tile in slopes:
            left_point = (tile.left, ground_y_on_slope(tile, tile.left))
            right_point = (tile.right, ground_y_on_slope(tile, tile.right))
            screen.draw.line(left_point, right_point, "magenta")
    screen.draw.text("Arrows to move, Up to jump, D to show slopes", (10, 10), color="black")


# updates game state between drawing of each frame
def update():
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
            # if it's not a short ledge to step up onto, it's a wall
            if not try_step_up(collided_platform):
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
            # if it's not a short ledge to step up onto, it's a wall
            if not try_step_up(collided_platform):
                fox.right = collided_platform.left
    # otherwise idle
    else:
        fox.sprite = fox_idle

    # remember if the fox started this frame on the ground (for walking downhill)
    was_on_ground = fox.on_ground
    # assume not on the ground unless a collision proves otherwise
    fox.on_ground = False
    # apply gravity
    fox.velocity_y += gravity
    # move vertically
    fox.y += fox.velocity_y

    # check slopes first, then platforms, so a platform wins where they meet
    land_on_slope(was_on_ground)

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

    # standing on a slope also stops vertical movement
    if fox.on_ground:
        fox.velocity_y = 0


# keyboard pressed event listener
def on_key_down(key):
    global show_slope_lines
    # up key and on the ground
    if key == keys.UP and fox.on_ground:
        fox.velocity_y = fox.jump_velocity
    # D key toggles the slope lines on and off
    if key == keys.D:
        show_slope_lines = not show_slope_lines


pgzrun.go()  # program must always end with this
