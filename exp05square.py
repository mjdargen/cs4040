# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this

# set width and height of screen
WIDTH = 500
HEIGHT = 500

# define Actor
alien = Actor("alien")
alien.topleft = (0, 0)
alien.velocity = 5

# global variables
state = 0


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    global state
    # move in a square
    # state 0: top horizontal part of square
    if state == 0:
        alien.x += alien.velocity
        # check rightmost part of Actor
        if alien.right >= WIDTH:
            state = 1
    # state 1: right vertical part of square
    elif state == 1:
        alien.y += alien.velocity
        # check bottommost part of Actor
        if alien.bottom >= HEIGHT:
            state = 2
    # state 2: bottom horizontal part of square
    elif state == 2:
        alien.x -= alien.velocity
        # check leftmost part of Actor
        if alien.left < 0:
            state = 3
    # state 3: left vertical part of square
    elif state == 3:
        alien.y -= alien.velocity
        # check bottommost part of Actor
        if alien.top < 0:
            state = 0


pgzrun.go()  # program must always end with this
