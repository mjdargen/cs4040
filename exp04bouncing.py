# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500

# define Actor
alien = Actor("alien")
# start actor at center
alien.midtop = (WIDTH // 2, HEIGHT // 2)

# choose a random velocity between -5 and 5 that is not zero
# defined as a tuple -> (x, y)
# x -> represents velocity or change in position for x direction
# y -> represents velocity or change in position for y direction
alien.velocity_x = randint(-5, 5)
alien.velocity_y = randint(-5, 5)
while alien.velocity_x == 0 or alien.velocity_y == 0:
    alien.velocity_x = randint(-5, 5)
    alien.velocity_y = randint(-5, 5)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    # modify position by velocity
    alien.x += alien.velocity_x
    alien.y += alien.velocity_y

    # check rightmost part of Actor
    if alien.right >= WIDTH:
        # bounce off right wall
        alien.velocity_x = -alien.velocity_x
    # check bottommost part of Actor
    elif alien.bottom >= HEIGHT:
        # bounce off bottom wall
        alien.velocity_y = -alien.velocity_y
    # check leftmost part of Actor
    elif alien.left < 0:
        # bounce off left wall
        alien.velocity_x = -alien.velocity_x
    # check bottommost part of Actor
    elif alien.top < 0:
        # bounce off top wall
        alien.velocity_y = -alien.velocity_y


pgzrun.go()  # program must always end with this
