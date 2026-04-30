import pgzrun
from pgzero.builtins import *
import random

# Pygame Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Inventory System"

# define global variables
alien = Actor("alien")
menu_button = Rect(10, 10, 120, 40)  # rectangle to represent our "button"
menu_item_actors = []  # list of actors to display in the menu
items = []  # list of items spawned in the game

# This is called a dictionary. It stores key, value pairs.
# Similar to list, but stores items with a key to refer to them.
# A key is what we use to retrieve the value, as opposed to the index.
# Prevents us from having to declare a bunch of lists and track which corresponds with which.
# We would have to a new list for each: names, quantities, and descriptions.
inventory = {
    "coin_gold": 0,
    "coin_silver": 0,
    "coin_bronze": 0,
    "gem_blue": 0,
    "gem_green": 0,
    "gem_red": 0,
    "gem_yellow": 0,
}
descriptions = {
    "coin_gold": "A shiny gold coin.",
    "coin_silver": "A silver coin.",
    "coin_bronze": "A worn bronze coin.",
    "gem_blue": "A bright blue gem.",
    "gem_green": "A smooth green gem.",
    "gem_red": "A deep red gem.",
    "gem_yellow": "A vibrant yellow gem.",
}


# runs once at beginning before draw()/update()
def start():
    alien.pos = (WIDTH / 2, HEIGHT / 2)
    setup_menu()
    clock.schedule_interval(spawn_random_item, 2.0)


# displays the new frame
def draw():
    # draw for during the game
    if game.state == "playing":
        screen.clear()  # clears the screen
        screen.fill("darkslateblue")  # fills background color
        alien.draw()  # draws the new sprite
        for item in items:
            item.draw()
        screen.draw.filled_rect(menu_button, "red")
        screen.draw.text("Menu", center=(70, 30), color="white", fontname="pixel_font")

    # draw for the paused menu screen
    if game.state == "paused":
        screen.clear()
        screen.fill("darkslateblue")
        screen.draw.text("Inventory", center=(WIDTH / 2, 50), color="white", fontname="pixel_font", fontsize=48)
        screen.draw.filled_rect(menu_button, "red")
        screen.draw.text("Resume", center=(70, 30), color="white", fontname="pixel_font")
        # for every type of item in the game
        for item in menu_item_actors:
            # draw it
            item.draw()
            # get the name of the item
            item_name = item.image
            # retrieve its quantity and description
            quantity = inventory[item_name]
            description = descriptions[item_name]
            # draw the quantity and use the item Actor position to determine where to draw
            screen.draw.text(
                str(quantity), midleft=(130, item.y - 12), color="white", fontname="pixel_font", fontsize=28
            )
            # draw the quantity and use the item Actor position to determine where to draw
            screen.draw.text(description, midleft=(130, item.y + 18), color="white", fontname="pixel_font", fontsize=22)


# updates game state between drawing of each frame
def update():
    if game.state != "playing":
        return
    # player movement
    if keyboard.LEFT:
        alien.x -= 10
    elif keyboard.RIGHT:
        alien.x += 10
    elif keyboard.UP:
        alien.y -= 10
    elif keyboard.DOWN:
        alien.y += 10
    # check if the movement caused a collision with an item
    collision_index = alien.collidelist(items)
    if collision_index != -1:
        # get which item the player collided with
        collided_item = items[collision_index]
        # get name of the item
        item_name = collided_item.image
        # update the quantity
        inventory[item_name] += 1
        # remove the collided item from the list so it no longer appears
        items.pop(collision_index)


# called when mouse button is pressed down
def on_mouse_down(pos, button):
    # check if left button was clicked where the "button" is,
    if button == mouse.LEFT and menu_button.collidepoint(pos):
        # if playing -> pause it
        if game.state == "playing":
            game.pause()
        # if paused -> resume it
        elif game.state == "paused":
            game.resume()


# function to setup the menu actors
def setup_menu():
    # if we ever restart, we should clear this out first
    menu_item_actors.clear()
    y_pos = 100  # starting y position
    # loop through each item in the inventory
    for item_name in inventory:
        # assign name and position
        item_actor = Actor(item_name)
        item_actor.x = 80
        item_actor.y = y_pos
        # append to list of item actors displayed in the menu
        menu_item_actors.append(item_actor)
        y_pos += 65  # move down every new item


# function to spawn a random item, scheduled in start
def spawn_random_item():
    # choose a name from the random list of keys for our inventory
    item_name = random.choice(list(inventory.keys()))
    # use that name to assign the actor image
    item = Actor(item_name)
    # choose random position
    item.x = random.randint(0, WIDTH)
    item.y = random.randint(0, HEIGHT)
    # append to list of items draw on the screen
    items.append(item)


pgzrun.go()
