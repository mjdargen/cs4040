import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Enemy AI Demo"

# define the Actors
player = Actor("alien_green")
enemy = Actor("alien_yellow")


# runs once at beginning before draw()/update()
def start():
    player.pos = (WIDTH / 2, 100)
    player.velocity = 5
    enemy.home = (150, 450)  # where the enemy starts its patrol
    enemy.pos = enemy.home
    # the enemy is always in one of these states: "patrol", "chase", or "return"
    enemy.state = "patrol"
    enemy.velocity_x = 2  # patrol speed (negative is left)
    enemy.chase_speed = 3  # slower than the player, so the player can escape
    enemy.sight = 150  # how close the player has to be for the enemy to see them
    enemy.give_up = 200  # how far away the player has to get for the enemy to stop chasing


# displays the new frame
def draw():
    screen.clear()
    screen.fill("forestgreen")
    # show how far the enemy can see, and what state it's in
    screen.draw.circle(enemy.pos, enemy.sight, "white")
    screen.draw.text(enemy.state, midbottom=(enemy.x, enemy.top - 5))
    enemy.draw()
    player.draw()
    if game.state == "lost":
        screen.draw.text("Caught!", center=(WIDTH / 2, HEIGHT / 2), fontsize=60)


# updates game state between drawing of each frame
def update():
    # if game state is not playing, just return
    if game.state != "playing":
        return
    move_player()
    move_enemy()
    # the enemy caught the player, lose and restart after 3 seconds
    if enemy.colliderect(player):
        game.lose(3.0)


# moves the player with the arrow keys, without going off the screen
def move_player():
    if keyboard.LEFT and player.left > 0:
        player.x -= player.velocity
    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity
    elif keyboard.UP and player.top > 0:
        player.y -= player.velocity
    elif keyboard.DOWN and player.bottom < HEIGHT:
        player.y += player.velocity


# moves the enemy "AI" based on what state it's in
def move_enemy():
    # how many pixels away the player is
    distance = enemy.distance_to(player)

    # patrol: walk back and forth between x = 150 and x = 650
    if enemy.state == "patrol":
        enemy.x += enemy.velocity_x
        if enemy.x >= 650:
            enemy.velocity_x = -2
        if enemy.x <= 150:
            enemy.velocity_x = 2
        # spotted the player, so start chasing
        if distance < enemy.sight:
            enemy.state = "chase"

    # chase: move straight toward the player
    elif enemy.state == "chase":
        enemy.move_toward(player, enemy.chase_speed)
        # the player got far enough away, so give up and go back home
        if distance > enemy.give_up:
            enemy.state = "return"

    # return: move straight back home, then start patrolling again
    elif enemy.state == "return":
        enemy.move_toward(enemy.home, enemy.chase_speed)
        if enemy.pos == enemy.home:
            enemy.state = "patrol"
        # spotted the player again on the way home
        if distance < enemy.sight:
            enemy.state = "chase"


pgzrun.go()
