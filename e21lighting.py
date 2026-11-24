import pgzrun
from pgzero.builtins import *
import random

# Pygame Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Lighting"

# define Sprites
torch_burn = Sprite(["torch1", "torch2"], fps=6)

# define the Actors
door = Actor("window")
crate = Actor("box_crate")
alien = Actor("alien_green")
bush = Actor("bush")
moon = Actor("moon_full")
left_torch = Actor(torch_burn)
right_torch = Actor(torch_burn)

# the ground, and the stone wall the torches hang on
ground = Rect(0, HEIGHT - 64, WIDTH, 64)
wall = Rect(140, HEIGHT - 280, 520, 216)

# global variables
darkness = 0.6  # how dark it is, from 0.0 (day) to 1.0 (pitch black)
flashlight_on = False
flashlight_pos = (WIDTH / 2, HEIGHT / 2)
torch_light_on = True
tint_color = "none"  # color drawn over everything, or "none"


# runs once at beginning before draw()/update()
def start():
    door.midbottom = (400, HEIGHT - 64)
    crate.scale = 0.6
    crate.midbottom = (80, HEIGHT - 64)
    alien.midbottom = (180, HEIGHT - 64)
    bush.midbottom = (700, HEIGHT - 64)
    moon.pos = (680, 110)
    left_torch.scale = 0.75
    left_torch.midbottom = (280, HEIGHT - 110)
    left_torch.brightness = 1.0  # how strong its light is, changed in update()
    right_torch.scale = 0.75
    right_torch.midbottom = (520, HEIGHT - 110)
    right_torch.brightness = 1.0


# displays the new frame
def draw():
    screen.clear()
    screen.fill("skyblue")
    # 1. the scene
    screen.draw.filled_rect(ground, "sienna")
    screen.draw.filled_rect(wall, "slategray")
    door.draw()
    crate.draw()
    alien.draw()
    bush.draw()
    moon.draw()
    # 2. darkness over the whole scene
    screen.draw.darkness(darkness)
    # 3. lights shine through the darkness, showing the real colors under them
    #    light(position, radius, color, opacity) - opacity makes a light weaker
    if torch_light_on:
        screen.draw.light(left_torch.pos, 130, "orange", opacity=left_torch.brightness)
        screen.draw.light(right_torch.pos, 130, "orange", opacity=right_torch.brightness)
    if flashlight_on:
        screen.draw.light(flashlight_pos, 150, "white")
    # the torches are drawn after the darkness, so they glow instead of being darkened
    left_torch.draw()
    right_torch.draw()
    # 4. a color tint: a see-through color over everything
    if tint_color != "none":
        screen.fill(tint_color, opacity=0.3)
    # 5. the controls, drawn last so they're always easy to read
    screen.draw.filled_rect(Rect(10, 10, 390, 110), "black", opacity=0.7)
    screen.draw.text("UP / DOWN: darkness " + str(darkness), (20, 20))
    screen.draw.text("F: flashlight (move the mouse) " + str(flashlight_on), (20, 45))
    screen.draw.text("T: torch light " + str(torch_light_on), (20, 70))
    screen.draw.text("1 2 3 4: tint " + tint_color, (20, 95))


# updates game state between drawing of each frame
def update():
    # make the torch light flicker like fire by changing its brightness every frame
    left_torch.brightness = random.uniform(0.7, 1.0)
    right_torch.brightness = random.uniform(0.7, 1.0)


# mouse moved event listener
def on_mouse_move(pos):
    global flashlight_pos
    # the flashlight shines wherever the mouse is
    flashlight_pos = pos


# keyboard pressed event listener
def on_key_down(key):
    global darkness, flashlight_on, torch_light_on, tint_color
    # darker or lighter, one step at a time (round keeps it to 1 decimal place)
    if key == keys.UP and darkness < 1:
        darkness = round(darkness + 0.1, 1)
    elif key == keys.DOWN and darkness > 0:
        darkness = round(darkness - 0.1, 1)
    # turn the flashlight and the torch light on or off
    elif key == keys.F:
        flashlight_on = not flashlight_on
    elif key == keys.T:
        torch_light_on = not torch_light_on
    # pick a tint
    elif key == keys.K_1:
        tint_color = "none"
    elif key == keys.K_2:
        tint_color = "navy"  # night
    elif key == keys.K_3:
        tint_color = "orange"  # sunset
    elif key == keys.K_4:
        tint_color = "red"  # alarm


pgzrun.go()  # program must always end with this
