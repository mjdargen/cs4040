import pgzrun
from pgzero.builtins import *
import random

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Start & Game Over with Collisions"

# define Actors, set positions in start()
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.velocity = 5
coin = Actor("coin_gold")
bomb = Actor("bomb")


# runs once at beginning before draw()/update()
def start():
    # set initial positions
    robot.pos = WIDTH // 2, HEIGHT // 2
    # reset variables for playing again
    robot.velocity = 5
    # set new position of bomb and coin
    move_bomb()
    move_coin()


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    coin.draw()
    bomb.draw()
    if game.state == "lost":
        screen.draw.text("Game over!", center=(WIDTH // 2, HEIGHT // 2))
    if game.state == "won":
        screen.draw.text("You won!", center=(WIDTH // 2, HEIGHT // 2))
    if game.state != "lost":
        robot.draw()
    screen.draw.text(f"Score: {game.score}", midleft=(20, 20))


# updates game state between drawing of each frame
def update():
    # do not execute update() if game is over
    if game.state != "playing":
        return
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
        game.score += 1
        if game.score >= 5:
            game.win(5.0)
    # if collision, trigger lose()
    if robot.colliderect(bomb):
        game.lose(5.0)


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        robot.image = "robot_idle"


# relocates coin to a new location
def move_coin():
    # randomly generate new position, 20 pixels from edge
    coin.x = random.randint(20, WIDTH - 20)
    coin.y = random.randint(20, HEIGHT - 20)
    # while coin is accidentally placed on bomb or robot, try new location
    while coin.colliderect(bomb) or coin.colliderect(robot):
        coin.x = random.randint(20, WIDTH - 20)
        coin.y = random.randint(20, HEIGHT - 20)


# relocates bomb to a new location
def move_bomb():
    # randomly generate new position, 20 pixels from edge
    bomb.x = random.randint(20, WIDTH - 20)
    bomb.y = random.randint(20, HEIGHT - 20)
    # while bomb is accidentally placed on robot or coin, try new location
    while bomb.colliderect(robot) or bomb.colliderect(coin):
        bomb.x = random.randint(20, WIDTH - 20)
        bomb.y = random.randint(20, HEIGHT - 20)


pgzrun.go()
