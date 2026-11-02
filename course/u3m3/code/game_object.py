# Code atom: the game object's attributes and the calls that change its state.
# Quoted by: u3m3-slides.qmd, u3m3-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "The game Object"


def start():
    # start snippet attributes
    game  # object that stores information about the game's state
    game.state  # str: "playing", "won", "lost", "over" or "paused"
    game.score  # int: starts at 0. Update it in your code.
    game.level  # int: starts at 1. Update it in your code.
    game.timer  # float: seconds since game started. Auto-updates.
    game.frame_count  # int: frames since game started. Auto-updates.
    # end snippet attributes


def game_reference():
    # Reference lines only: this function is never called.
    # start snippet end
    # each one also cancels everything scheduled on the clock
    game.win()  # sets game.state to "won"
    game.lose()  # sets game.state to "lost"
    game.over()  # sets game.state to "over"
    # end snippet end
    # start snippet pause
    game.pause()  # sets game.state to "paused"
    game.resume()  # sets game.state back to "playing"
    # end snippet pause
    # start snippet restart
    game.win(2.5)  # like game.win(), then restart after 2.5 seconds
    game.lose(3)  # like game.lose(), then restart after 3 seconds
    game.over(5)  # like game.over(), then restart after 5 seconds
    # end snippet restart


def draw():
    screen.clear()
    screen.draw.text(f"State: {game.state}", center=(WIDTH // 2, 200))
    screen.draw.text(f"Time: {game.timer:.2f}", center=(WIDTH // 2, 250))
    screen.draw.text(f"Frames: {game.frame_count}", center=(WIDTH // 2, 300))


def update():
    if game.timer > 5:
        game.over(3)


pgzrun.go()
