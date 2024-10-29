import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500
TITLE = "List Collectibles"

# define Actor
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.velocity = 5

# global variables
over = False
coins = []  # create list
timer = 0
score = 0


# called at the beginning and when reset
def start():
    global timer, over, score
    over = False
    robot.pos = WIDTH // 2, HEIGHT // 2
    coins.clear()  # remove all elements from list
    timer = 0
    score = 0
    clock.schedule_interval(increment_timer, 1.0)
    clock.schedule_interval(spawn_coin, 0.5)


# called during lose condition to trigger game_over and schedule start again
def game_over():
    global over
    # set over to True
    over = True
    # schedule start to run in 5 seconds
    clock.schedule_unique(start, 5.0)
    # stop increment counter, will be scheduled again in start
    clock.unschedule(increment_timer)
    clock.unschedule(spawn_coin)


# timer increment event handler
def increment_timer():
    global timer
    timer += 1


# spawn coin event handler
def spawn_coin():
    coin = Actor("coin_gold")
    coin.x = randint(40, WIDTH - 40)
    coin.y = randint(40, HEIGHT - 40)
    coins.append(coin) # add new coin to list


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    robot.draw()
    # draw all coins in the list
    for coin in coins:
        coin.draw()
    screen.draw.text(f"Score: {score}", midleft=(20, 20))
    screen.draw.text(f"Time: {timer}", midright=(WIDTH - 20, 20))
    if over:
        screen.draw.text("Game over!", center=(WIDTH // 2, HEIGHT // 2))


# updates game state between drawing of each frame
def update():
    global score
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
        score += 1
        
    # once there are more than 5 coins call game over
    if len(coins) > 5 and not over:
        game_over()


# released key event listener
def on_key_up(key):
    robot.image = "robot_idle"


start()
pgzrun.go()
