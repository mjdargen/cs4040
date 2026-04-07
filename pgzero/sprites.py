import pygame

from . import loaders
from .actor import Actor, POS_TOPLEFT, ANCHOR_CENTER


class SpriteSheet:
    def __init__(self, name):
        self.name = name
        self.sheet = loaders.sprites.load(name)

    def image_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        return image

    def images_at(self, rects, color_key=None):
        return [self.image_at(rect, color_key) for rect in rects]

    def load_strip(self, rect, image_count, color_key=None):
        rects = [
            (rect[0] + rect[2] * i, rect[1], rect[2], rect[3])
            for i in range(image_count)
        ]
        return self.images_at(rects, color_key)


class Sprite:
    def __init__(
        self,
        image_name,
        frame_width,
        frame_height,
        row_number,
        frame_count,
        fps=10,
        transparent_color=None,
    ):
        self.image_name = image_name
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.row_number = row_number
        self.frame_count = frame_count
        self.fps = fps
        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()

        ss = SpriteSheet(image_name)
        first_rect = (
            0,
            frame_height * row_number,
            frame_width,
            frame_height,
        )
        self.images = ss.load_strip(first_rect, frame_count, transparent_color)

        if not self.images:
            raise ValueError("Sprite must contain at least one frame")

    @property
    def image(self):
        return self.images[self.frame_index]

    def reset(self):
        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()

    def next_frame(self):
        current_time = pygame.time.get_ticks()
        frame_duration_ms = 1000 / self.fps

        if current_time - self.last_update_time >= frame_duration_ms:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.last_update_time = current_time

        return self.images[self.frame_index]


class SpriteActor(Actor):
    def __init__(
        self,
        sprite,
        pos=POS_TOPLEFT,
        anchor=ANCHOR_CENTER,
        collision_rect=None,
        **kwargs,
    ):
        self._sprite = sprite
        self._paused = False

        super().__init__(
            sprite.image,
            pos=pos,
            anchor=anchor,
            collision_rect=collision_rect,
            **kwargs,
        )

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        old_sprite = self._sprite
        self._sprite = sprite
        if old_sprite is not sprite:
            self._sprite.reset()
        self.image = self._sprite.image

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    @property
    def paused(self):
        return self._paused

    def update_animation(self):
        if not self._paused:
            self.image = self._sprite.next_frame()

    def draw(self):
        self.update_animation()
        super().draw()
