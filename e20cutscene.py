import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Cutscene"

# define Sprites
crab_idle = Sprite("crab", frame_width=32, frame_height=16, row=0, frames=4, fps=5)
crab_walk = Sprite("crab", frame_width=32, frame_height=16, row=1, frames=4, fps=8)
crab = Actor(crab_idle)  # player
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=2)
fox_walk = Sprite("fox", frame_width=24, frame_height=16, row=2, frames=8, fps=10)
fox = Actor(fox_idle)  # only appears in the cutscene

# the beach the crab is trying to reach, on the right side of the screen
beach = Rect(WIDTH - 120, 0, 120, HEIGHT)

# an invisible line across the screen: walking into it starts the cutscene
cutscene_trigger = Rect(350, 0, 10, HEIGHT)

# black bars at the top and bottom of the screen during the cutscene, like a movie
top_bar = Rect(0, 0, WIDTH, 80)
bottom_bar = Rect(0, HEIGHT - 120, WIDTH, 120)

# global variables
cutscene_step = 0  # which step of the cutscene is playing (0 means not started yet)
caption = ""  # text shown during the cutscene ("" means no text)


# runs once at beginning before draw()/update()
def start():
    crab.scale = 3
    crab.pos = (100, 300)
    crab.velocity = 4
    fox.scale = 3
    fox.left = WIDTH  # waits just off the right side of the screen
    fox.flip_h = True  # face left, toward the crab


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    screen.draw.filled_rect(beach, "sandybrown")
    crab.draw()
    fox.draw()

    # during the cutscene, draw the black bars and the caption over top
    if game.state == "cutscene":
        screen.draw.filled_rect(top_bar, "black")
        screen.draw.filled_rect(bottom_bar, "black")
        if caption != "":
            screen.draw.text(
                caption,
                topleft=(bottom_bar.left + 30, bottom_bar.top + 25),
                width=bottom_bar.width - 60,
                color="white",
                fontname="pixel_font",
                fontsize=28,
            )
            screen.draw.text(
                "SPACE to continue",
                bottomright=(bottom_bar.right - 15, bottom_bar.bottom - 10),
                color="gray",
                fontname="pixel_font",
                fontsize=18,
            )
    elif game.state == "won":
        screen.draw.text("You made it!", center=(WIDTH / 2, HEIGHT / 2), fontname="pixel_font")


# updates game state between drawing of each frame
def update():
    if game.state == "playing":
        player_movement()
    elif game.state == "cutscene":
        play_cutscene()


# moves the player with the arrow keys, and checks what they walked into
def player_movement():
    if keyboard.LEFT:
        crab.x -= crab.velocity
        crab.sprite = crab_walk
    elif keyboard.RIGHT:
        crab.x += crab.velocity
        crab.sprite = crab_walk
    elif keyboard.UP:
        crab.y -= crab.velocity
        crab.sprite = crab_walk
    elif keyboard.DOWN:
        crab.y += crab.velocity
        crab.sprite = crab_walk
    else:
        crab.sprite = crab_idle

    # crab walked into the trigger, start the cutscene (only if it hasn't played yet)
    if crab.colliderect(cutscene_trigger) and cutscene_step == 0:
        crab.sprite = crab_idle
        fox.y = crab.y  # the fox comes in at the same height as the crab
        game.state = "cutscene"

    # crab reached the beach, win
    if crab.colliderect(beach):
        crab.sprite = crab_idle
        game.win()


# plays the cutscene one step at a time
# a step either moves something until it gets where it's going,
# or shows a caption until the player presses SPACE (see on_key_down)
def play_cutscene():
    global cutscene_step, caption
    # step 0: the fox walks in from the right until it's next to the crab
    if cutscene_step == 0:
        fox.sprite = fox_walk
        fox.x -= 3
        if fox.left <= crab.right + 20:
            fox.sprite = fox_idle
            cutscene_step = 1
    # step 1: the fox talks
    elif cutscene_step == 1:
        caption = "Fox: Little crab! The tide is going out without you!"
    # step 2: the crab answers
    elif cutscene_step == 2:
        caption = "Crab: Oh no! I have to get back to the beach!"
    # step 3: the fox runs off the right side of the screen
    elif cutscene_step == 3:
        caption = ""
        fox.flip_h = False  # face right
        fox.sprite = fox_walk
        fox.x += 6
        if fox.left > WIDTH:
            cutscene_step = 4
    # step 4: the cutscene is over, so the player takes control again
    # (cutscene_step stays at 4, so the trigger won't start it again)
    elif cutscene_step == 4:
        game.state = "playing"


# keyboard pressed event listener
def on_key_down(key):
    global cutscene_step
    # during the cutscene, SPACE moves past a caption to the next step
    if key == keys.SPACE and game.state == "cutscene" and caption != "":
        cutscene_step += 1


pgzrun.go()  # program must always end with this
