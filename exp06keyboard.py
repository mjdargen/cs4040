# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this

# set width and height of screen
WIDTH = 600
HEIGHT = 300

# define Actors
bg = Actor("grass", (WIDTH // 2, HEIGHT // 2))
robot = Actor("robot_idle")
robot.midbottom = WIDTH // 2, HEIGHT

# define velocities and gravity
gravity = 1
velocity_x = 0
velocity_y = 0


# displays the new frame
def draw():
    screen.clear()
    bg.draw()
    robot.draw()


# updates game state between drawing of each frame
def update():
    global velocity_x, velocity_y
    # while left key is pressed and not at edge
    if keyboard.LEFT and robot.midleft[0] > 0:
        # show left facing image and change x velocity
        robot.image = "robot_left"
        velocity_x = -5
    # while right key is pressed and not at edge
    elif keyboard.RIGHT and robot.midright[0] < WIDTH:
        # show right facing image and change x velocity
        robot.image = "robot_right"
        velocity_x = 5
    # otherwise set x velocity to 0
    else:
        velocity_x = 0

    # change y velocity by adding gravity
    # causes deceleration in the upwards direction
    # causes acceleration in the downwards direction
    velocity_y += gravity

    # modify robot position by the velocity
    robot.x += velocity_x
    robot.y += velocity_y

    # once the robot has returned to the floor, cancel y velocity
    # robot.midbottom[1] gives bottommost part of actor
    if robot.midbottom[1] >= HEIGHT:
        velocity_y = 0
        robot.midbottom = robot.x, HEIGHT


# called when a keyboard button is pressed
def on_key_down(key):
    global velocity_y
    # change vertical velocity when space or up keys are pressed
    # make sure not previously jumping first
    if (key == keys.SPACE or key == keys.UP) and velocity_y == 0:
        velocity_y = -10


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        robot.image = "robot_idle"


pgzrun.go()  # program must always end with this