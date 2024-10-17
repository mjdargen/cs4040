import pgzrun  # program must always start with this

# set width and height of screen
WIDTH = 500
HEIGHT = 500
TITLE = "Start & Game Over"

# global variables
over = False
countdown_timer = 10

# define Actor
robot = Actor("robot_idle")


# contains code for setting up game, must be called below!
def start():
    global countdown_timer, over
    robot.pos = WIDTH // 2, HEIGHT // 2  # set initial pos
    countdown_timer = 10  # reset timer
    over = False  # set over to False
    # schedule countdown timer
    clock.schedule_interval(decrement_timer, 1.0)


# scheduled callback for decrementing counter every second
def decrement_timer():
    global countdown_timer, over
    countdown_timer -= 1  # decrement counter


# called during lose condition to trigger game_over and schedule start again
def game_over():
    global over
    over = True  # set over to True
    # schedule start to run in 2 seconds
    clock.schedule_unique(start, 2.0)
    # stop decrement counter, will be scheduled again in start
    clock.unschedule(decrement_timer)


# displays the new frame
def draw():
    screen.clear()
    robot.draw()
    # show countdown timer if game is live
    if not over:
        screen.draw.text(f"Time: {countdown_timer}", center=(WIDTH // 2, 20))
    # show game over if timer elapsed
    else:
        screen.draw.text("Game Over", center=(WIDTH // 2, 20))


# updates game state between drawing of each frame
def update():
    # once timer has elapsed, call game_over()
    if countdown_timer == 0:
        game_over()


start()  # call start just before pgzrun.go()
pgzrun.go()  # program must always end with this
