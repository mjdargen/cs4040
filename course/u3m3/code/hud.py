# Code atom: a heads-up display (HUD) drawn at the end of draw().
# Quoted by: u3m3-slides.qmd, u3m3-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "Heads-Up Display"


# start snippet draw
def draw():
    screen.clear()
    # ... draw the actors and scene here, then the HUD on top
    screen.draw.text(f"Score: {game.score}", midleft=(20, 20))
    screen.draw.text(f"Time: {int(game.timer)}", center=(WIDTH // 2, 20))
    screen.draw.text(f"Level: {game.level}", midright=(WIDTH - 20, 20))
    if game.state == "lost":
        screen.draw.text("Game over!", center=(WIDTH // 2, HEIGHT // 2))
    if game.state == "won":
        screen.draw.text("You won!", center=(WIDTH // 2, HEIGHT // 2))
# end snippet draw


def update():
    if game.timer > 10:
        game.win(3)


pgzrun.go()
