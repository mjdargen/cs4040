import pgzrun  # program must always start with this
from random import randint

# set width and height of screen
WIDTH = 500
HEIGHT = 500
TITLE = "Frame Counter"

# global variables towards the top of the program
# defined outside of functions
alien = Actor("alien_beige_stand")
alien.pos = (WIDTH // 2, HEIGHT // 2)

# declare global variable to keep track of frame
frame = 0

# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    alien.draw()  # draws the new sprite


# updates game state between drawing of each frame
def update():
    # must indicate frame is global because we're modifying it
    global frame
    # make something occur every ten frames
    if frame % 10 == 0:
        # change from stand to jump
        if alien.image == "alien_beige_stand":
            alien.image = "alien_beige_jump"
        # change from jump to stand
        elif alien.image == "alien_beige_jump":
            alien.image = "alien_beige_stand"
    # increment our frame count by 1 every time update executes
    frame += 1


pgzrun.go()  # program must always end with this
