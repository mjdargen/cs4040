# Code atom: playing background music with the music object.
# Quoted by: u4m2-slides.qmd, u4m2-cheatsheet.qmd
# "interlude" and "jam" are example names: this repo has no music/ folder, so
# the names are fine as given. To run this, put interlude.mp3 and jam.mp3
# (or .ogg) in music/.
import pgzrun
from pgzero.builtins import *

WIDTH = 500
HEIGHT = 300
TITLE = "Music"


def start():
    # start snippet play
    music.play("interlude")  # plays file "interlude" on a loop
    music.play_once("interlude")  # plays file "interlude" once
    music.queue("jam")  # queues "jam" to play after the current track
    music.is_playing()  # returns True if music is playing
    music.stop()  # stops the music
    # end snippet play
    # start snippet status
    music.is_playing("jam")  # returns True if "jam" is playing
    music.is_paused()  # returns True if the music is paused
    # end snippet status
    # start snippet control
    music.pause()  # pauses the current track
    music.unpause()  # resumes the current track
    music.fadeout(2.5)  # fades out the current track over 2.5 seconds
    music.set_volume(0.5)  # sets volume to 0.5 (0 = silent, 1 = max)
    music.get_volume()  # gets the current volume setting
    # end snippet control


def draw():
    screen.clear()


pgzrun.go()
