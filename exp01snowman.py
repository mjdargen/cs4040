import pgzrun
from pgzero.builtins import *

# set width and height of screen
WIDTH = 600
HEIGHT = 400
TITLE = "Snowman"

# color reference: https://pygame-zero.readthedocs.io/en/latest/colors_ref.html


# displays the new frame
def draw():
    screen.clear()
    # draw background
    screen.fill("skyblue")
    # rectangle = Rect((x, y), (width, height))
    # x, y is the coordinate of the top-left corner.
    rectangle = Rect((0, 300), (WIDTH, 100))  # At top of code with actors
    screen.draw.filled_rect(rectangle, "snow")
    # screen.draw.line((x1, y1), (x2, y2), "color")
    screen.draw.line((0, 300), (WIDTH, 300), "black")

    # draw snowman body
    # screen.draw.circle((x,y), radius, color)
    # x, y is the coordinate of the center.
    screen.draw.filled_circle((WIDTH // 2, 275), 75, "white")  # draws filled circle
    screen.draw.circle((WIDTH // 2, 275), 75, "black")  # draws circular outline
    screen.draw.filled_circle((WIDTH // 2, 150), 50, "white")  # draws filled circle
    screen.draw.circle((WIDTH // 2, 150), 50, "black")  # draws circular outline
    screen.draw.filled_circle((WIDTH // 2, 60), 40, "white")  # draws filled circle
    screen.draw.circle((WIDTH // 2, 60), 40, "black")  # draws circular outline

    # draw face
    # eyes
    screen.draw.filled_circle((WIDTH // 2 - 15, 45), 5, "black")  # draws filled circle
    screen.draw.filled_circle((WIDTH // 2 + 15, 45), 5, "black")  # draws filled circle
    # nose
    screen.draw.filled_circle((WIDTH // 2, 60), 5, "orange")  # draws filled circle
    # mouth
    screen.draw.filled_circle((WIDTH // 2 - 4, 80), 4, "black")  # draws filled circle
    screen.draw.filled_circle((WIDTH // 2 + 4, 80), 4, "black")  # draws filled circle
    screen.draw.filled_circle((WIDTH // 2 - 12, 77), 4, "black")  # draws filled circle
    screen.draw.filled_circle((WIDTH // 2 + 12, 77), 4, "black")  # draws filled circle
    screen.draw.filled_circle((WIDTH // 2 - 20, 74), 4, "black")  # draws filled circle
    screen.draw.filled_circle((WIDTH // 2 + 20, 74), 4, "black")  # draws filled circle

    # draw arms
    # compute with code
    left_start = (WIDTH // 2 - 40, 150)
    left_end = (left_start[0] - 60, left_start[1] - 40)
    right_start = (WIDTH // 2 + 40, 150)
    right_end = (right_start[0] + 60, right_start[1] - 40)
    screen.draw.line(left_start, left_end, "black")
    screen.draw.line(right_start, right_end, "black")
    # or compute by hand, does same thing as above
    screen.draw.line((260, 150), (200, 110), "black")
    screen.draw.line((340, 150), (400, 110), "black")


# updates game state between drawing of each frame
def update():
    pass  # pass means do nothing, used because we can't have empty function


pgzrun.go()  # program must always end with this
