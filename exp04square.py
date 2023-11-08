# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this

# set width and height of screen
WIDTH = 500
HEIGHT = 500

# define Actor
alien = Actor("alien")
alien.topleft = 0, 0

state = 0
velocity = 5


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
        alien.x += velocity
        # check rightmost part of Actor aka alien.midright[0]
        if alien.midright[0] >= WIDTH:
            state = 1
    # state 1: right vertical part of square
    elif state == 1:
        alien.y += velocity
        # check bottommost part of Actor aka alien.midbottom[0]
        if alien.midbottom[1] >= HEIGHT:
            state = 2
    # state 2: bottom horizontal part of square
    elif state == 2:
        alien.x -= velocity
        # check leftmost part of Actor aka alien.midleft[0]
        if alien.midleft[0] < 0:
            state = 3
    # state 3: left vertical part of square
    elif state == 3:
        alien.y -= velocity
        # check bottommost part of Actor aka alien.midtop[0]
        if alien.midtop[1] < 0:
            state = 0


pgzrun.go()  # program must always end with this
