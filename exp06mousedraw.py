# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this

# set width and height of screen
WIDTH = 500
HEIGHT = 500

# declare global variables
current_point = (0, 0)
previous_point = (0, 0)
clear = True

# displays the new frame
def draw():
    global clear
    if clear:
        screen.clear()
        screen.fill("white")
        clear = False
    # between each of the points, draw a black line
    screen.draw.line(previous_point, current_point, "black")


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, used because we can't have empty function


# mouse event handler
def on_mouse_down(pos, button):
    global current_point, previous_point, clear
    if button == mouse.LEFT:
        previous_point = current_point
        current_point = pos
    elif button == mouse.RIGHT:
        clear = True  # signal to draw() to clear the screen
        current_point = (0, 0)
        previous_point = (0, 0)


pgzrun.go()  # program must always end with this
