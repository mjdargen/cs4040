from . import clock
from . import music
from . import tone
from .actor import Actor
from .storage import storage
from .keyboard import keyboard
from .animation import animate
from .rect import Rect, ZRect
from .loaders import images, sounds
from .constants import mouse, keys, keymods
from .game import exit

from typing import TYPE_CHECKING
from .screen import Screen
from .screen import screen_instance as screen
if TYPE_CHECKING:
    screen: Screen  # Type hint for IDEs and static analyzers


__all__ = [
    'screen', 'Screen',  # graphics output
    'Actor', 'images',  # graphics
    'sounds', 'music', 'tone',  # sound
    'clock', 'animate',  # timing
    'Rect', 'ZRect',  # geometry
    'keyboard', 'mouse', 'keys', 'keymods',  # input
    'storage',  # persistence
    'exit',
]