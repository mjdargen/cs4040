import pgzrun
from pgzero.builtins import *

# Pygame Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Dialogue"

# define Sprites
crab_idle = Sprite("crab", frame_width=32, frame_height=16, row=0, frames=4, fps=5)
crab_walk = Sprite("crab", frame_width=32, frame_height=16, row=1, frames=4, fps=8)
crab = Actor(crab_idle)  # player
frog_idle = Sprite("frog", frame_width=24, frame_height=24, row=0, frames=7, fps=5)
frog = Actor(frog_idle)  # NPC
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=2)
fox = Actor(fox_idle)  # NPC

# All the dialogue in the game is stored in a dictionary, like the inventory in e18.
# key: the name of a character
# value: a list of the lines in their conversation, in order
# To add another character's dialogue, add another key and list.
dialogue = {
    "frog": [
        "Frog: Ribbit! I haven't seen a crab in this pond before.",
        "Crab: I'm lost. Do you know the way to the beach?",
        "Frog: I don't, but the fox might. Foxes go everywhere.",
    ],
    "fox": [
        "Fox: ...",
        "Crab: Excuse me, do you know the way to the beach?",
        "Fox: Follow the river east until you smell salt water.",
        "Crab: Thanks!",
    ],
}

# box at the bottom of the screen where the dialogue is shown
dialogue_box = Rect(20, HEIGHT - 170, WIDTH - 40, 150)

# global variables
talking = False  # is a conversation happening right now?
conversation = []  # list of lines in the current conversation
line_index = 0  # which line of the conversation is showing


# runs once at beginning before draw()/update()
def start():
    crab.scale = 3
    crab.pos = (100, 50)
    crab.velocity = 4
    # the frog is first along the path, then the fox further on
    frog.scale = 3
    frog.pos = (350, 150)
    frog.flip_h = True  # face left, toward the crab
    fox.scale = 3
    fox.pos = (650, 350)
    fox.flip_h = True  # face left, toward the crab


def draw_dialogue_box():
    # during a conversation, show the current line in the dialogue box
    if talking:
        screen.draw.filled_rect(dialogue_box, "black")
        screen.draw.rect(dialogue_box, "white")  # white border around the box
        # the current line (width wraps long lines so they fit in the box)
        screen.draw.text(
            conversation[line_index],
            topleft=(dialogue_box.left + 20, dialogue_box.top + 20),
            width=dialogue_box.width - 40,
            color="white",
            fontname="pixel_font",
            fontsize=28,
        )
        screen.draw.text(
            "SPACE to continue",
            bottomright=(dialogue_box.right - 15, dialogue_box.bottom - 10),
            color="gray",
            fontname="pixel_font",
            fontsize=18,
        )
    # otherwise, tell the player they can talk when they're touching a character
    elif crab.colliderect(frog):
        screen.draw.text(
            "SPACE to talk",
            midbottom=(frog.x, frog.top - 10),
            color="white",
            fontname="pixel_font",
            fontsize=24,
        )
    elif crab.colliderect(fox):
        screen.draw.text(
            "SPACE to talk",
            midbottom=(fox.x, fox.top - 10),
            color="white",
            fontname="pixel_font",
            fontsize=24,
        )


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("darkslateblue")  # fills background color
    frog.draw()
    fox.draw()
    crab.draw()
    draw_dialogue_box()


# updates game state between drawing of each frame
def update():
    # the player can't move during a conversation
    if talking:
        crab.sprite = crab_idle
        return

    # player movement
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


# keyboard pressed event listener
def on_key_down(key):
    global talking, conversation, line_index
    if key == keys.SPACE:
        # already talking: move on to the next line
        if talking:
            line_index += 1
            # no lines left, so the conversation is over
            if line_index == len(conversation):
                talking = False
        # not talking yet: start a conversation with the character the crab is touching
        # by looking up their conversation in the dialogue dictionary
        elif crab.colliderect(frog):
            conversation = dialogue["frog"]
            line_index = 0
            talking = True
        elif crab.colliderect(fox):
            conversation = dialogue["fox"]
            line_index = 0
            talking = True


pgzrun.go()  # program must always end with this
