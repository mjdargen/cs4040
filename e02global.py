import pgzrun
from pgzero.builtins import *
import random

# Pygame Constants
WIDTH = 500
HEIGHT = 500
TITLE = "Global Variables"

# global variables towards the top of the program
# defined outside of functions
alien = Actor("alien")
alien.pos = (200, 200)
n = 3
m = 5
text = "ha"
result_text = ""
words = []

# Rules:
# When do you need global?
#  You do NOT need global if:
#   - You are only reading the variable
#   - You are modifying something inside the variable (like a list or object)
#  You DO need global if:
#   - You are reassigning the variable to a new value
#   - Common for int, float, bool, string, tuple when changed


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    # alien is an Object and not reassigned, does not need global keyword
    # words is a list and not reassigned, does not need global keyword
    # m is an int and is reassigned, so it needs the global keyword
    # result_text is a string and is reassigned, so it needs the global keyword
    # n is an int but is only read, so it does not need the global keyword
    # text is a string but is only read, so it does not need the global keyword
    global m, result_text
    m += n
    result_text += text
    words.append(text)
    alien.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)


pgzrun.go()  # program must always end with this
