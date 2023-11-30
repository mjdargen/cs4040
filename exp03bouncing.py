# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500

# define Actor
alien = Actor("alien")
# start actor at center
alien.midtop = WIDTH // 2, HEIGHT // 2

# choose a random velocity between -5 and 5 that is not zero
# defined as a tuple -> (x, y)
# x -> represents velocity or change in position for x direction
# y -> represents velocity or change in position for y direction
velocity_x = randint(-5, 5)
velocity_y = randint(-5, 5)
while velocity_x == 0 or velocity_y == 0:
    velocity_x = randint(-5, 5)
    velocity_y = randint(-5, 5)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    global velocity_x, velocity_y
    # modify position by velocity
    alien.x += velocity_x
    alien.y += velocity_y

    # check rightmost part of Actor
    if alien.right >= WIDTH:
        # bounce off right wall
        velocity_x = -velocity_x
    # check bottommost part of Actor
    elif alien.bottom >= HEIGHT:
        # bounce off bottom wall
        velocity_y = -velocity_y
    # check leftmost part of Actor
    elif alien.left < 0:
        # bounce off left wall
        velocity_x = -velocity_x
    # check bottommost part of Actor
    elif alien.top < 0:
        # bounce off top wall
        velocity_y = -velocity_y


pgzrun.go()  # program must always end with this
