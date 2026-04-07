import builtins as python_builtins

# Expose clock API as a builtin
from . import clock
from . import music
from . import tone
from .actor import Actor
from .sprites import Sprite, SpriteActor
from .storage import storage
from .keyboard import keyboard
from .animation import animate
from .rect import Rect, ZRect
from .loaders import images, sounds
from .constants import mouse, keys, keymods
from .game import Game, exit
from .tilemaps import load_tile_map_actors

# The actual screen will be installed here
from .screen import screen_instance as screen

# Global game state object
game = getattr(python_builtins, "game", Game())


__all__ = [
    "screen",  # graphics output
    "Actor",
    "images",
    "Sprite",
    "SpriteActor",  # graphics
    "sounds",
    "music",
    "tone",  # sound
    "clock",
    "animate",  # timing
    "Rect",
    "ZRect",  # geometry
    "keyboard",
    "mouse",
    "keys",
    "keymods",  # input
    "storage",  # persistence
    "Game",
    "game",
    "exit",
    "load_tile_map_actors",
]
