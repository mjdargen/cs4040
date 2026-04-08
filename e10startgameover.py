import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Start & Game Over"

# global variables
countdown_timer = 5
# define Actor
robot = Actor("robot_idle")


# runs once at beginning before draw()/update()
def start():
    global countdown_timer
    # set initial pos
    robot.pos = (WIDTH // 2, HEIGHT // 2)
    # reset timer
    countdown_timer = 5
    # reset and restart the game state
    game.restart()
    # schedule countdown timer
    clock.schedule_interval(decrement_timer, 1.0)


# scheduled callback for decrementing counter every second
def decrement_timer():
    global countdown_timer
    countdown_timer -= 1  # decrement counter


# called during lose condition to trigger game_over and schedule start again
def game_over():
    # immediately return and don't run code if game already over!
    if game.state == "game_over":
        return
    # set state to be game over
    game.state = "game_over"
    # schedule start to run in 2 seconds
    clock.schedule_unique(start, 2.0)
    # stop decrement counter, will be scheduled again in start
    clock.unschedule(decrement_timer)


# displays the new frame
def draw():
    screen.clear()
    robot.draw()
    # show countdown timer if game is live
    if game.state == "playing":
        screen.draw.text(f"Time: {countdown_timer}", center=(WIDTH // 2, 20))
    # show game over if timer elapsed
    else:
        screen.draw.text("Game Over", center=(WIDTH // 2, 20))


# updates game state between drawing of each frame
def update():
    # once timer has elapsed, call game_over()
    if countdown_timer <= 0:
        game_over()


pgzrun.go()
