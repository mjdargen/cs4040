# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this

# set width and height of screen
WIDTH = 500
HEIGHT = 500

points = []
clicked = False


# displays the new frame
def draw():
    screen.clear()
    screen.fill("white")
    # between each of the points, draw a black line
    for i in range(len(points) - 1):
        screen.draw.line(points[i], points[i + 1], "black")


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, used because we can't have empty function


def on_mouse_down():
    global clicked
    clicked = True  # set to true to signal to on_mouse_move
    points.clear()  # clear list of points


def on_mouse_up():
    global clicked
    clicked = False  # set to true to signal to on_mouse_move


def on_mouse_move(pos):
    # if mouse is clicked, add positions to be drawn
    if clicked:
        points.append(pos)


pgzrun.go()  # program must always end with this
