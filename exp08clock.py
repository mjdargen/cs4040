import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500
TITLE = "Clock Example"

# define Actor
robot = Actor("robot_idle", (WIDTH // 2, HEIGHT // 2))
timer = 0


# displays the new frame
def draw():
    screen.clear()
    screen.fill("darkslateblue")
    robot.draw()
    screen.draw.text(f"Time: {timer}", center=(WIDTH // 2, 20))


# updates game state between drawing of each frame
def update():
    pass


# scheduled callback for incrementing timer counter
def increment_timer():
    global timer
    timer += 1


# scheduled callback for moving character to a random position
def move_character():
    robot.x = randint(50, WIDTH - 50)
    robot.y = randint(50, HEIGHT - 50)


# call just before pgzrun.go() to schedule intervals
# otherwise, they would be repeatedly scheduled
clock.schedule_interval(increment_timer, 1.0)
clock.schedule_interval(move_character, 2.0)
pgzrun.go()  # program must always end with this
