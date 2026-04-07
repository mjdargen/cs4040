import pgzrun
from pgzero.builtins import *
import random

# set width and height of screen
WIDTH = 500
HEIGHT = 500
TITLE = "Music and Sounds"

# define Actors, set positions in start()
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.velocity = 5
coin = Actor("coin_gold")
bomb = Actor("bomb")


# runs once at beginning before draw()/update()
def start():
    # reset variables for playing again
    robot.velocity = 5
    # reset and restart the game state
    game.restart()
    # set initial positions
    robot.pos = WIDTH // 2, HEIGHT // 2
    move_bomb()
    move_coin()
    # start music
    music.play("house")


# called during lose condition to trigger game_over and schedule start again
def game_over():
    # immediately return and don't run code if game already over!
    if game.state == "game_over":
        return
    # play bomb sound
    sounds.bomb_explosion.play()
    # set state to be game over
    game.state = "game_over"
    # schedule start to run in 2 seconds
    clock.schedule_unique(start, 5.0)
    # stop music
    music.stop()
    # schedule game over sound for after bomb explosion ends
    clock.schedule_unique(game_over_sound, sounds.bomb_explosion.get_length())


# callback function for scheduling game over sound
def game_over_sound():
    sounds.gameover.play()


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


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    coin.draw()
    bomb.draw()
    if game.state == "game_over":
        screen.draw.text("Game over!", center=(WIDTH // 2, HEIGHT // 2))
    else:
        robot.draw()


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
        sounds.find_money.play()
        move_coin()
    # if collision, trigger game_over()
    if robot.colliderect(bomb):
        game_over()


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        robot.image = "robot_idle"


start()
pgzrun.go()
