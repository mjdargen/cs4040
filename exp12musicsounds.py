# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500

# define Actors, set positions in start()
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.velocity = 5
coin = Actor("coin_gold")
bomb = Actor("bomb")

# global variables
over = False
timer = 0


# called at start or restart of game to reinitialize
def start():
    # include and reset global variables for playing again
    global over, timer
    robot.velocity = 5
    over = False
    timer = 0
    # set initial positions
    robot.pos = WIDTH // 2, HEIGHT // 2
    move_bomb()
    move_coin()
    # set interval timers
    clock.schedule_interval(increment_timer, 1.0)
    # start music
    music.play("house")


# scheduled callback for incrementing counter every second
def increment_timer():
    global timer
    timer += 1  # increment counter


# called during lose condition to trigger game_over and schedule start again
def game_over():
    global over
    # set over to True
    over = True
    # schedule start to run in 2 seconds
    clock.schedule_unique(start, 5.0)
    # stop increment counter, will be scheduled again in start
    clock.unschedule(increment_timer)
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
        bomb.x = randint(20, WIDTH - 20)
        bomb.y = randint(20, HEIGHT - 20)


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    coin.draw()
    bomb.draw()
    if over:
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
    # if collision and not already game over, trigger game_over()
    if robot.colliderect(bomb) and not over:
        sounds.bomb_explosion.play()
        game_over()


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        robot.image = "robot_idle"


start()
pgzrun.go()
