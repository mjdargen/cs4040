import pgzrun
from pgzero.builtins import *
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500
TITLE = "Collision Example"

# define player Actor
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.pos = (WIDTH // 2, HEIGHT // 2)
robot.velocity = 5

# create coin Actor
coin = Actor("coin_gold")
# position is set by calling move_coin() just before pgzrun.go()

# create bomb Actor
bomb = Actor("bomb")
# position is set by calling move_bomb() just before pgzrun.go()


# relocates coin to a new location
def move_coin():
    # randomly generate new position, 20 pixels from edge
    coin.x = randint(20, WIDTH - 20)
    coin.y = randint(20, HEIGHT - 20)
    # while coin is accidentally placed on bomb or robot, try new location
    while coin.colliderect(bomb) or coin.colliderect(robot):
        coin.x = randint(20, WIDTH - 20)
        coin.y = randint(20, HEIGHT - 20)


# relocates bomb to a new location
def move_bomb():
    # randomly generate new position, 20 pixels from edge
    bomb.x = randint(20, WIDTH - 20)
    bomb.y = randint(20, HEIGHT - 20)
    # while bomb is accidentally placed on robot or coin, try new location
    while bomb.colliderect(robot) or bomb.colliderect(coin):
        coin.x = randint(20, WIDTH - 20)
        coin.y = randint(20, HEIGHT - 20)


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    robot.draw()
    coin.draw()
    bomb.draw()


# updates game state between drawing of each frame
def update():
    # while left key is pressed and not at edge
    if keyboard.LEFT and robot.left > 0:
        # show left facing image and change x velocity
        robot.image = "robot_left"
        robot.x -= robot.velocity
    # while right key is pressed and not at edge
    elif keyboard.RIGHT and robot.right < WIDTH:
        # show right facing image and change x velocity
        robot.image = "robot_right"
        robot.x += robot.velocity
    # while UP key is pressed and not at edge
    elif keyboard.UP and robot.top > 0:
        robot.y -= robot.velocity
    # while DOWN key is pressed and not at edge
    elif keyboard.DOWN and robot.bottom < HEIGHT:
        robot.y += robot.velocity

    # if collision with coin, add a new coin
    if robot.colliderect(coin):
        move_coin()
    # if collision with bomb, start over, move player to start
    if robot.colliderect(bomb):
        robot.pos = WIDTH // 2, HEIGHT // 2


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        robot.image = "robot_idle"


move_bomb()
move_coin()
pgzrun.go()
