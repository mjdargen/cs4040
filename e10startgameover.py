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
    # schedule countdown timer
    clock.schedule_interval(decrement_timer, 1.0)


# scheduled callback for decrementing counter every second
def decrement_timer():
    global countdown_timer
    countdown_timer -= 1  # decrement counter


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
    # once timer has elapsed, trigger game_over()
    if countdown_timer <= 0:
        game.game_over()


pgzrun.go()
