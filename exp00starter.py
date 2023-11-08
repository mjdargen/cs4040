# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Name of Game"

# define Actor
alien = Actor("alien")
alien.pos = 200, 200


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, used because we can't have empty function


pgzrun.go()  # program must always end with this
