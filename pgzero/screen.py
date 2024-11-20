import pygame
import pygame.draw
from . import ptext
from .rect import RECT_CLASSES
from . import loaders


def round_pos(pos):
    """Round a tuple position so it can be used for drawing."""
    x, y = pos
    return round(x), round(y)


def make_color(arg):
    if isinstance(arg, tuple):
        return arg
    return tuple(pygame.Color(arg))


class SurfacePainter:
    """Interface to pygame.draw that is bound to a surface with alpha support."""

    def __init__(self, screen):
        self._screen = screen

    @property
    def _surf(self):
        return self._screen.surface

    def _apply_alpha_drawing(self, draw_fn, *args, **kwargs):
        """Helper function to handle drawing with alpha support."""
        temp_surface = pygame.Surface(self._surf.get_size(), flags=pygame.SRCALPHA)
        temp_surface = temp_surface.convert_alpha()
        draw_fn(temp_surface, *args, **kwargs)
        self._surf.blit(temp_surface, (0, 0))

    def line(self, start, end, color):
        """Draw a line from start to end with alpha support."""
        start = round_pos(start)
        end = round_pos(end)
        self._apply_alpha_drawing(pygame.draw.line, make_color(color), start, end, 1)

    def circle(self, pos, radius, color):
        """Draw a circle with alpha support."""
        pos = round_pos(pos)
        self._apply_alpha_drawing(pygame.draw.circle, make_color(color), pos, radius, 1)

    def filled_circle(self, pos, radius, color):
        """Draw a filled circle with alpha support."""
        pos = round_pos(pos)
        self._apply_alpha_drawing(pygame.draw.circle, make_color(color), pos, radius, 0)

    def rect(self, rect, color):
        """Draw a rectangle with alpha support."""
        if not isinstance(rect, RECT_CLASSES):
            raise TypeError("screen.draw.rect() requires a rect to draw")
        self._apply_alpha_drawing(pygame.draw.rect, make_color(color), rect, 1)

    def filled_rect(self, rect, color):
        """Draw a filled rectangle with alpha support."""
        if not isinstance(rect, RECT_CLASSES):
            raise TypeError("screen.draw.filled_rect() requires a rect to draw")
        self._apply_alpha_drawing(pygame.draw.rect, make_color(color), rect, 0)

    def text(self, *args, **kwargs):
        """Draw text to the screen with alpha support."""
        temp_surface = pygame.Surface(self._surf.get_size(), flags=pygame.SRCALPHA)
        temp_surface = temp_surface.convert_alpha()
        ptext.draw(*args, surf=temp_surface, **kwargs)
        self._surf.blit(temp_surface, (0, 0))

    def textbox(self, *args, **kwargs):
        """Draw text wrapped in a box to the screen with alpha support."""
        temp_surface = pygame.Surface(self._surf.get_size(), flags=pygame.SRCALPHA)
        temp_surface = temp_surface.convert_alpha()
        ptext.drawbox(*args, surf=temp_surface, **kwargs)
        self._surf.blit(temp_surface, (0, 0))


class Screen:
    """Interface to the screen."""

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

    def clear(self):
        """Clear the screen to black."""
        self.fill((0, 0, 0))

    def fill(self, color):
        """Fill the screen with a colour."""
        self.surface.fill(make_color(color))

    def blit(self, image, pos):
        """Draw a sprite onto the screen.

        "blit" is an archaic name for this operation, but one that is is still
        frequently used, for example in Pygame. See the `Wikipedia article`__
        for more about the etymology of the term.

        .. __: http://en.wikipedia.org/wiki/Bit_blit

        :param image: A Surface or the name of an image object to load.
        :param pos: The coordinates at which the top-left corner of the sprite
                    will be positioned. This may be given as a pair of
                    coordinates or as a Rect. If a Rect is given the sprite
                    will be drawn at ``rect.topleft``.

        """
        if isinstance(image, str):
            image = loaders.images.load(image)
        self.surface.blit(image, pos)

    @property
    def draw(self):
        return SurfacePainter(self)
