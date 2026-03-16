import pgzrun
from pgzero.builtins import *

# Pygame constants
WIDTH = 600
HEIGHT = 200
TITLE = "Projectile Demo"

player = Actor("alien_beige")
player.bottomleft = (0, HEIGHT)
player.velocity_x = 0
player.velocity_y = 0

enemy = Actor("alien_yellow")
enemy.bottomright = (WIDTH, HEIGHT)

gravity = 1
projectiles = []


# displays the new frame
def draw():
    screen.clear()
    screen.fill("black")
    player.draw()
    enemy.draw()
    for projectile in projectiles:
        projectile.draw()


# updates game state between drawing of each frame
def update():
    # while left key is pressed and not at edge
    if keyboard.LEFT and player.left > 0:
        player.velocity_x = -5
    # while right key is pressed and not at edge
    elif keyboard.RIGHT and player.right < WIDTH:
        player.velocity_x = 5
    # otherwise set x velocity to 0
    else:
        player.velocity_x = 0

    # modify player position by the velocity
    player.x += player.velocity_x
    player.y += player.velocity_y

    # handle gravity
    # once the player has returned to the floor, cancel y velocity
    if player.bottom >= HEIGHT:
        player.velocity_y = 0
        player.y = HEIGHT - player.height / 2
    # otherwise, continue to add gravity
    # change y velocity by adding gravity
    # causes deceleration in the upwards direction
    # causes acceleration in the downwards direction
    else:
        player.velocity_y += gravity

    # update projectile position
    for projectile in projectiles:
        projectile.x += 5
        # remove if gone off the screen
        if projectile.left > WIDTH:
            projectiles.remove(projectile)

    # check if enemy hit by projectile
    collision_index = enemy.collidelist(projectiles)
    if collision_index != -1:
        # remove from list
        projectiles.pop(collision_index)
        # begin death animation
        clock.schedule_interval(death_animation, 0.2)


# callback function for death animation
def death_animation():
    # fall off screen
    enemy.y += 20
    # unschedule once they fall of screen / schedule respawn
    if enemy.top > HEIGHT:
        clock.unschedule(death_animation)
        clock.schedule_unique(respawn_enemy, 2.0)


# callback function to respawn enemy
def respawn_enemy():
    enemy.bottomright = (WIDTH, HEIGHT)


# called when a keyboard button is pressed
def on_key_down(key):
    # change vertical velocity when up key is pressed
    # make sure not previously jumping first
    if key == keys.UP and player.bottom >= HEIGHT:
        player.velocity_y = -10
    # create new projectile to player's right
    if key == keys.SPACE:
        projectile = Actor("fireball_small")
        projectile.midleft = player.midright
        projectiles.append(projectile)


pgzrun.go()
