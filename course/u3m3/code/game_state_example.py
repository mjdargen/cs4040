# Code atom: using game.state in draw() and update(), with win/lose restarts.
# Quoted by: u3m3-slides.qmd, u3m3-cheatsheet.qmd
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 500
TITLE = "Game State Example"

player = Actor("robot_idle")
enemy = Actor("bomb")
key = Actor("key_yellow")

# start snippet program
# start snippet start
def start():  # runs at the beginning and again on every restart
    player.pos = (200, 200)
    enemy.pos = (400, 400)
    key.pos = (450, 200)  # reach the key to win
# end snippet start


# start snippet draw
def draw():
    screen.clear()
    key.draw()
    if game.state != "lost":  # draw player if "playing" or "won"
        player.draw()
    if game.state != "won":  # draw enemy if "playing" or "lost"
        enemy.draw()
    if game.state == "won":
        screen.draw.text("You won!", midtop=(250, 20))
    if game.state == "lost":
        screen.draw.text("Game over", midtop=(250, 20))
# end snippet draw


# start snippet update
def update():
    if game.state != "playing":  # not playing: skip the rest
        return
    player.x += 1
    if player.colliderect(enemy):
        game.lose(5)  # "lost", then restart after 5 seconds
    if player.colliderect(key):
        game.win(3)  # "won", then restart after 3 seconds
# end snippet update
# end snippet program


pgzrun.go()
