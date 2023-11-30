import os
import time
import pygame
from pgzero import game, loaders
from pgzero.builtins import Actor
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def build(filename, tile_size):
    with open(f"{DIR_PATH}/{filename}", "r") as f:
        contents = f.read().splitlines()

    # convert to int but check if valid and for negative numbers
    contents = [c.split(",") for c in contents]
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            val = contents[row][col]
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                contents[row][col] = int(val)

    # create all items as Actors
    items = []
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            tile_num = contents[row][col]
            if tile_num != -1:
                # https://doc.mapeditor.org/en/stable/reference/global-tile-ids/
                flipped_h = bool(tile_num & 0x80000000)
                flipped_v = bool(tile_num & 0x40000000)
                flipped_d = bool(tile_num & 0x20000000)
                rotated_hex = bool(tile_num & 0x10000000)
                tile_num &= 0x0FFFFFFF
                item = Actor(f"tiles/tile_{tile_num:04d}")
                if flipped_d:
                    item.flip_d = True
                if flipped_h:
                    item.flip_x = True
                if flipped_v:
                    item.flip_y = True
                if rotated_hex:
                    pass
                item.topleft = (tile_size * col, tile_size * row)
                items.append(item)

    return items


# https://www.pygame.org/wiki/Spritesheet
class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except pygame.error as message:
            print(message)

    def image_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    def images_at(self, rects, color_key=None):
        return [self.image_at(rect, color_key) for rect in rects]

    def load_strip(self, rect, image_count, color_key=None):
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, color_key)


class Sprite(object):
    def __init__(self, filename, rect, count, color_key=None, frames=1):
        self.filename = filename
        ss = SpriteSheet(f"./images/sprites/{filename}")
        self.images = ss.load_strip(rect, count, color_key)
        self.i = 0
        self.frames = frames
        self.frame_num = frames

    def next(self):
        if self.frame_num == 0:
            self.i = (self.i + 1) % len(self.images)
            self.frame_num = self.frames
        else:
            self.frame_num -= 1
        return self.images[self.i]


class Actor(Actor):
    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._flip_x = False
        self._flip_y = False
        self._flip_d = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5
        self.direction = 0
        super().__init__(image, pos, anchor, **kwargs)

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        self._images = images
        if len(self._images) != 0:
            self.image = self._images[0]

    def next_image(self):
        if self.image in self._images:
            current = self._images.index(self.image)
            if current == len(self._images) - 1:
                self.image = self._images[0]
            else:
                self.image = self._images[current + 1]
        else:
            self.image = self._images[0]

    def animate(self):
        now = int(time.time() * self.fps)
        if now != self._animate_counter:
            self._animate_counter = now
            self.next_image()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self._transform_surf()

    @property
    def flip_x(self):
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x):
        self._flip_x = flip_x
        self._transform_surf()

    @property
    def flip_y(self):
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y):
        self._flip_y = flip_y
        self._transform_surf()

    @property
    def flip_d(self):
        return self._flip_d

    @flip_d.setter
    def flip_d(self, flip_d):
        self._flip_d = flip_d
        self._transform_surf()

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        self._orig_surf = self._surf = loaders.images.load(image)
        self._update_pos()
        self._transform_surf()

    def _transform_surf(self):
        self._surf = self._orig_surf
        p = self.pos

        if self._scale != 1:
            size = self._orig_surf.get_size()
            self._surf = pygame.transform.scale(
                self._surf, (int(size[0] * self.scale), int(size[1] * self.scale))
            )
        # flip_x - flips horizontally, about y-axis
        if self._flip_x:
            self._surf = pygame.transform.flip(self._surf, True, False)
        # flip_y - flips vertically, about x-axis
        if self._flip_y:
            self._surf = pygame.transform.flip(self._surf, False, True)
        # flips diagonally
        if self._flip_d:
            self._surf = pygame.transform.rotate(self._surf, 90)
            self._surf = pygame.transform.flip(self._surf, True, False)

        self._surf = pygame.transform.rotate(self._surf, self._angle)

        self.width, self.height = self._surf.get_size()
        w, h = self._orig_surf.get_size()
        ax, ay = self._untransformed_anchor
        anchor = transform_anchor(ax, ay, w, h, self._angle)
        self._anchor = (anchor[0] * self.scale, anchor[1] * self.scale)

        self.pos = p
        self._mask = None

    def draw(self):
        game.screen.blit(self._surf, self.topleft)


class SpriteActor(Actor):
    def __init__(self, sprite, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._flip_x = False
        self._flip_y = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5
        self.direction = 0
        self.sprite = sprite
        super().__init__(f"sprites/{sprite.filename}", pos, anchor, **kwargs)
        self._orig_surf = self.sprite.images[self.sprite.i]
        self._update_pos()
        self._transform_surf()

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        self._images = images
        if len(self._images) != 0:
            self.image = self._images[0]

    def next_image(self):
        if self.image in self._images:
            current = self._images.index(self.image)
            if current == len(self._images) - 1:
                self.image = self._images[0]
            else:
                self.image = self._images[current + 1]
        else:
            self.image = self._images[0]

    def animate(self):
        now = int(time.time() * self.fps)
        if now != self._animate_counter:
            self._animate_counter = now
            self.next_image()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self._transform_surf()

    @property
    def flip_x(self):
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x):
        self._flip_x = flip_x
        self._transform_surf()

    @property
    def flip_y(self):
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y):
        self._flip_y = flip_y
        self._transform_surf()

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    @property
    def image(self):
        return self._image_name

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        self._orig_surf = self._surf = loaders.images.load(image)
        self._update_pos()
        self._transform_surf()

    def _transform_surf(self):
        self._surf = self._orig_surf
        p = self.pos

        if self._scale != 1:
            size = self._orig_surf.get_size()
            self._surf = pygame.transform.scale(
                self._surf, (int(size[0] * self.scale), int(size[1] * self.scale))
            )
        if self._flip_x:
            self._surf = pygame.transform.flip(self._surf, True, False)
        if self._flip_y:
            self._surf = pygame.transform.flip(self._surf, False, True)

        self._surf = pygame.transform.rotate(self._surf, self._angle)

        self.width, self.height = self._surf.get_size()
        w, h = self._orig_surf.get_size()
        ax, ay = self._untransformed_anchor
        anchor = transform_anchor(ax, ay, w, h, self._angle)
        self._anchor = (anchor[0] * self.scale, anchor[1] * self.scale)

        self.pos = p
        self._mask = None

    def draw(self):
        if self.sprite:
            if self.sprite.frame_num == 0:
                self.sprite.i = (self.sprite.i + 1) % len(self.sprite.images)
                self.sprite.frame_num = self.sprite.frames
            else:
                self.sprite.frame_num -= 1
            self._orig_surf = self._surf = self.sprite.images[self.sprite.i]
            self._update_pos()
            self._transform_surf()
            game.screen.blit(self._surf, self.topleft)
        else:
            game.screen.blit(self._surf, self.topleft)
