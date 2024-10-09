import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
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
"""
Rules for when global keyword is needed:
- Never need global keyword for objects, lists, dictionaries, etc.
- Need global keyword for int, float, bool, string, tuple, but if and only if the variables are modified!
"""


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    # alien is an Object, does not need global keyword
    # words is a list, does not need global keyword
    # m is an int and is modified, so it needs the global keyword
    # result_text is a string and is modified, so it needs the global keyword
    # n is an int but is not modified, so it does not need the global keyword
    # text is a string but is not modified, so it does not need the global keyword
    global m, result_text
    m += n
    result_text += text
    words.append(text)
    alien.pos = randint(0, WIDTH), randint(0, HEIGHT)


pgzrun.go()  # program must always end with this
