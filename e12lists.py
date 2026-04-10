import pgzrun
from pgzero.builtins import *
import random

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "List Collectibles"

# global variables
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.velocity = 5
coins = []  # create list


# runs once at beginning before draw()/update()
def start():
    robot.pos = WIDTH // 2, HEIGHT // 2
    coins.clear()  # remove all elements from list
    # schedule coins to begin spawning
    clock.schedule_interval(spawn_coin, 0.5)


# spawn coin event handler
def spawn_coin():
    coin = Actor("coin_gold")
    coin.x = random.randint(40, WIDTH - 40)
    coin.y = random.randint(40, HEIGHT - 40)
    coins.append(coin)  # add new coin to list


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    robot.draw()
    # draw all coins in the list
    for coin in coins:
        coin.draw()
    screen.draw.text(f"Score: {game.score}", midleft=(20, 20))
    screen.draw.text(f"Time: {int(game.timer)}", midright=(WIDTH - 20, 20))
    if game.state == "lost":
        screen.draw.text("Game over!", center=(WIDTH // 2, HEIGHT // 2))
    if game.state == "won":
        screen.draw.text("You won!", center=(WIDTH // 2, HEIGHT // 2))


# updates game state between drawing of each frame
def update():
    # do not execute update() if game is over
    if game.state != "playing":
        return
    if keyboard.LEFT and robot.left > 0:
        robot.x -= robot.velocity
        robot.image = "robot_left"
    elif keyboard.RIGHT and robot.right < WIDTH:
        robot.x += robot.velocity
        robot.image = "robot_right"
    elif keyboard.UP and robot.top > 0:
        robot.y -= robot.velocity
    elif keyboard.DOWN and robot.bottom < HEIGHT:
        robot.y += robot.velocity

    # check for collision between robot and any coins
    collided_index = robot.collidelist(coins)
    if collided_index != -1:
        coins.pop(collided_index)
        game.score += 1
        if game.score >= 5:
            game.win(3.0)

    # once there are more than 5 coins call game over
    if len(coins) > 5:
        game.lose(3.0)


# released key event listener
def on_key_up(key):
    robot.image = "robot_idle"


pgzrun.go()
