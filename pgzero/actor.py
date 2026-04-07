import time
import pygame
from math import radians, sin, cos, atan2, degrees, sqrt

from . import game
from . import loaders
from . import rect
from . import spellcheck


ANCHORS = {
    "x": {
        "left": 0.0,
        "center": 0.5,
        "middle": 0.5,
        "right": 1.0,
    },
    "y": {
        "top": 0.0,
        "center": 0.5,
        "middle": 0.5,
        "bottom": 1.0,
    },
}


def calculate_anchor(value, dim, total):
    if isinstance(value, str):
        try:
            return total * ANCHORS[dim][value]
        except KeyError:
            raise ValueError("%r is not a valid %s-anchor name" % (value, dim))
    return float(value)


# These are methods (of the same name) on pygame.Rect
SYMBOLIC_POSITIONS = set(
    (
        "topleft",
        "bottomleft",
        "topright",
        "bottomright",
        "midtop",
        "midleft",
        "midbottom",
        "midright",
        "center",
    )
)

# Provides more meaningful default-arguments e.g. for display in IDEs etc.
POS_TOPLEFT = None
ANCHOR_CENTER = None

MAX_ALPHA = 255  # Based on pygame's max alpha.


def transform_anchor(ax, ay, w, h, angle):
    """Transform anchor based upon a rotation of a surface of size w x h."""
    theta = -radians(angle)

    sintheta = sin(theta)
    costheta = cos(theta)

    # Dims of the transformed rect
    tw = abs(w * costheta) + abs(h * sintheta)
    th = abs(w * sintheta) + abs(h * costheta)

    # Offset of the anchor from the center
    cax = ax - w * 0.5
    cay = ay - h * 0.5

    # Rotated offset of the anchor from the center
    rax = cax * costheta - cay * sintheta
    ray = cax * sintheta + cay * costheta

    return (tw * 0.5 + rax, th * 0.5 + ray)


def _set_opacity(actor, current_surface):
    alpha = int(actor.opacity * MAX_ALPHA + 0.5)

    if alpha == MAX_ALPHA:
        return current_surface

    alpha_img = pygame.Surface(current_surface.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, alpha))
    alpha_img.blit(
        current_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
    )
    return alpha_img


def _set_scale(actor, current_surface):
    if actor._scale == 1.0:
        return current_surface

    w, h = current_surface.get_size()
    sw = max(1, int(round(w * actor._scale)))
    sh = max(1, int(round(h * actor._scale)))
    return pygame.transform.scale(current_surface, (sw, sh))


def _set_flip(actor, current_surface):
    surf = current_surface

    if actor._flip_d:
        surf = pygame.transform.rotate(surf, -90)
        surf = pygame.transform.flip(surf, True, False)

    if actor._flip_h or actor._flip_v:
        surf = pygame.transform.flip(surf, actor._flip_h, actor._flip_v)

    return surf


def _set_angle(actor, current_surface):
    if actor._angle % 360 == 0:
        return current_surface
    return pygame.transform.rotate(current_surface, actor._angle)


class Actor:
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS
    DELEGATED_ATTRIBUTES = [a for a in dir(rect.ZRect) if not a.startswith("_")]

    function_order = [_set_opacity, _set_scale, _set_flip, _set_angle]

    _anchor = _anchor_value = (0, 0)
    _angle = 0.0
    _opacity = 1.0
    _scale = 1.0
    _flip_h = False
    _flip_v = False
    _flip_d = False
    _images = []
    _animate_counter = 0
    fps = 5
    direction = 0
    _sprite = None
    _collision_rect_spec = None
    _collision_rect = None

    def _build_transformed_surf(self):
        cache_len = len(self._surface_cache)
        if cache_len == 0:
            last = self._orig_surf
        else:
            last = self._surface_cache[-1]

        for f in self.function_order[cache_len:]:
            new_surf = f(self, last)
            self._surface_cache.append(new_surf)
            last = new_surf

        return self._surface_cache[-1]

    def __init__(
        self,
        image,
        pos=POS_TOPLEFT,
        anchor=ANCHOR_CENTER,
        collision_rect=None,
        **kwargs
    ):
        self._handle_unexpected_kwargs(kwargs)

        self._surface_cache = []
        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))
        self._collision_rect_spec = collision_rect
        self._collision_rect = None
        self._mask = None

        self.image = image
        self._init_position(pos, anchor, **kwargs)
        self._update_collision_rect()

    def __getattr__(self, attr):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return setattr(self._rect, attr, value)
        else:
            return object.__setattr__(self, attr, value)

    def __iter__(self):
        return iter(self._rect)

    def __repr__(self):
        return "<{} {!r} pos={!r}>".format(
            type(self).__name__, self._image_name, self.pos
        )

    def __dir__(self):
        standard_attributes = [
            key for key in self.__dict__.keys() if not key.startswith("_")
        ]
        return standard_attributes + self.__class__.DELEGATED_ATTRIBUTES

    def _handle_unexpected_kwargs(self, kwargs):
        unexpected_kwargs = set(kwargs.keys()) - self.EXPECTED_INIT_KWARGS
        if not unexpected_kwargs:
            return

        typos, _ = spellcheck.compare(
            unexpected_kwargs, self.EXPECTED_INIT_KWARGS
        )
        for found, suggested in typos:
            raise TypeError(
                "Unexpected keyword argument '{}' (did you mean '{}'?)".format(
                    found, suggested
                )
            )

    def _init_position(self, pos, anchor, **kwargs):
        if anchor is None:
            anchor = ("center", "center")
        self.anchor = anchor

        symbolic_pos_args = {
            k: kwargs[k] for k in kwargs if k in SYMBOLIC_POSITIONS
        }

        if not pos and not symbolic_pos_args:
            self.topleft = (0, 0)
        elif pos and symbolic_pos_args:
            raise TypeError(
                "'pos' argument cannot be mixed with 'topleft', "
                "'topright' etc. argument."
            )
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

    def _set_symbolic_pos(self, symbolic_pos_dict):
        if len(symbolic_pos_dict) == 0:
            raise TypeError(
                "No position-setting keyword arguments ('topleft', "
                "'topright' etc) found."
            )
        if len(symbolic_pos_dict) > 1:
            raise TypeError(
                "Only one 'topleft', 'topright' etc. argument is allowed."
            )

        setter_name, position = symbolic_pos_dict.popitem()
        setattr(self, setter_name, position)

    def _update_transform(self, function):
        if function in self.function_order:
            i = self.function_order.index(function)
            del self._surface_cache[i:]
            self._mask = None
        else:
            raise IndexError(
                "function {!r} does not have a registered order."
                "".format(function)
            )

    @property
    def anchor(self):
        return self._anchor_value

    @anchor.setter
    def anchor(self, val):
        self._anchor_value = val
        self._calc_anchor()

    def _calc_anchor(self):
        ax, ay = self._anchor_value
        ow, oh = self._orig_surf.get_size()

        ax = calculate_anchor(ax, "x", ow)
        ay = calculate_anchor(ay, "y", oh)
        self._untransformed_anchor = ax, ay

        transformed_w = ow * self._scale
        transformed_h = oh * self._scale

        if self._flip_d:
            transformed_w, transformed_h = transformed_h, transformed_w

        if self._angle == 0.0:
            self._anchor = (
                ax * self._scale,
                ay * self._scale,
            )
            if self._flip_d:
                self._anchor = transform_anchor(
                    ax * self._scale,
                    ay * self._scale,
                    ow * self._scale,
                    oh * self._scale,
                    -90,
                )
        else:
            anchor_x = ax * self._scale
            anchor_y = ay * self._scale

            if self._flip_d:
                anchor_x, anchor_y = transform_anchor(
                    anchor_x,
                    anchor_y,
                    ow * self._scale,
                    oh * self._scale,
                    -90,
                )

            self._anchor = transform_anchor(
                anchor_x,
                anchor_y,
                transformed_w,
                transformed_h,
                self._angle,
            )

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        p = self.pos
        self._update_pos()
        self.pos = p
        self._update_transform(_set_angle)
        self._update_collision_rect()

    @property
    def opacity(self):
        """Get/set the current opacity value."""
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        self._opacity = min(1.0, max(0.0, opacity))
        self._update_transform(_set_opacity)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        p = self.pos
        self._update_pos()
        self.pos = p
        self._update_transform(_set_scale)
        self._update_collision_rect()

    @property
    def flip_h(self):
        return self._flip_h

    @flip_h.setter
    def flip_h(self, value):
        self._flip_h = value
        p = self.pos
        self._update_pos()
        self.pos = p
        self._update_transform(_set_flip)
        self._update_collision_rect()

    @property
    def flip_v(self):
        return self._flip_v

    @flip_v.setter
    def flip_v(self, value):
        self._flip_v = value
        p = self.pos
        self._update_pos()
        self.pos = p
        self._update_transform(_set_flip)
        self._update_collision_rect()

    @property
    def flip_d(self):
        return self._flip_d

    @flip_d.setter
    def flip_d(self, value):
        self._flip_d = value
        p = self.pos
        self._update_pos()
        self.pos = p
        self._update_transform(_set_flip)
        self._update_collision_rect()

    @property
    def pos(self):
        px, py = self.topleft
        ax, ay = self._anchor
        return px + ax, py + ay

    @pos.setter
    def pos(self, pos):
        px, py = pos
        ax, ay = self._anchor
        self.topleft = px - ax, py - ay

    def rect(self):
        return self._rect.copy()

    @property
    def x(self):
        ax = self._anchor[0]
        return self.left + ax

    @x.setter
    def x(self, px):
        self.left = px - self._anchor[0]

    @property
    def y(self):
        ay = self._anchor[1]
        return self.top + ay

    @y.setter
    def y(self, py):
        self.top = py - self._anchor[1]

    @property
    def image(self):
        if self._image_name is not None:
            return self._image_name
        return self._orig_surf

    @image.setter
    def image(self, image):
        if isinstance(image, pygame.Surface):
            self._image_name = None
            self._orig_surf = image
        else:
            self._image_name = image
            self._orig_surf = loaders.images.load(image)

        self._surface_cache.clear()
        self._update_pos()
        self._update_collision_rect()

    def _update_pos(self):
        p = getattr(self, "pos", (0, 0))

        base_w, base_h = self._orig_surf.get_size()
        w = base_w * self._scale
        h = base_h * self._scale

        if self._flip_d:
            w, h = h, w

        if self._angle != 0.0:
            ra = radians(self._angle)
            sin_a = sin(ra)
            cos_a = cos(ra)
            self.height = abs(w * sin_a) + abs(h * cos_a)
            self.width = abs(w * cos_a) + abs(h * sin_a)
        else:
            self.width = w
            self.height = h

        self._calc_anchor()
        self.pos = p

    def draw(self):
        self._update_collision_rect()
        s = self._build_transformed_surf()
        game.screen.blit(s, self.topleft)

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        self._images = images
        if self._images:
            self.image = self._images[0]

    def next_image(self):
        if not self._images:
            return

        if self.image in self._images:
            current = self._images.index(self.image)
            self.image = self._images[(current + 1) % len(self._images)]
        else:
            self.image = self._images[0]

    def animate(self):
        now = int(time.time() * self.fps)
        if now != self._animate_counter:
            self._animate_counter = now
            self.next_image()

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        self._sprite = sprite

    def _update_collision_rect(self):
        if self._collision_rect_spec is None:
            self._collision_rect = self._rect.copy()
        elif len(self._collision_rect_spec) == 2:
            cw, ch = self._collision_rect_spec
            cw *= self._scale
            ch *= self._scale
            cx, cy = self.center
            tlx = cx - cw / 2
            tly = cy - ch / 2
            self._collision_rect = rect.ZRect(tlx, tly, cw, ch)
        elif len(self._collision_rect_spec) == 4:
            top, right, bottom, left = self._collision_rect_spec
            top *= self._scale
            right *= self._scale
            bottom *= self._scale
            left *= self._scale
            cx, cy = self.center
            tlx = cx - left
            tly = cy - top
            cw = left + right
            ch = top + bottom
            self._collision_rect = rect.ZRect(tlx, tly, cw, ch)
        else:
            raise ValueError(
                "Invalid collision_rect_spec format. "
                "Use (width, height) or (top, right, bottom, left)."
            )

    def colliderect(self, other):
        my_rect = (
            self._rect
            if self._collision_rect_spec is None
            else self._collision_rect
        )

        if (
            hasattr(other, "_collision_rect_spec")
            and other._collision_rect_spec is not None
        ):
            other_rect = other._collision_rect
        elif hasattr(other, "_rect"):
            other_rect = other._rect
        else:
            other_rect = other

        return my_rect.colliderect(other_rect)

    def collidelist(self, others):
        for n, other in enumerate(others):
            if self.colliderect(other):
                return n
        return -1

    def collidepoint(self, *args):
        r = (
            self._rect
            if self._collision_rect_spec is None
            else self._collision_rect
        )
        return r.collidepoint(*args)

    @property
    def collision_rect(self):
        if self._collision_rect_spec is None:
            return self._rect
        return self._collision_rect

    @collision_rect.setter
    def collision_rect(self, value):
        self._collision_rect_spec = value
        self._update_collision_rect()

    def draw_collision_rect(self):
        r = self.collision_rect
        pygame.draw.rect(
            game.screen,
            (255, 0, 0),
            (r.x, r.y, r.w, r.h),
            2,
        )

    def angle_to(self, target):
        """Return the angle from this actors position to target, in degrees."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = myy - ty
        return degrees(atan2(dy, dx))

    def distance_to(self, target):
        """Return the distance from this actor's pos to target, in pixels."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = ty - myy
        return sqrt(dx * dx + dy * dy)

    def unload_image(self):
        if self._image_name is not None:
            loaders.images.unload(self._image_name)
