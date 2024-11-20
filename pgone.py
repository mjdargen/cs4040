import os
import time
import pygame
from pgzero import game, loaders
from pgzero.builtins import Actor
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def build(csv_path, tile_size, scale=1):
    """
    Builds a list of Pygame Zero Actors from a tilesheet and a CSV tile map from Tiled.

    Args:
        csv_path (str): The relative path to the CSV file containing the tilemap data.
        tile_size (int): The size (width and height) of each tile in pixels.
        scale (float, optional): The scaling factor for the tiles. Defaults to 1.

    Returns:
        list: A list of `Actor` objects representing the tilemap.

    The CSV file should contain integers representing tile indices. Negative values
    are ignored, and special flags for tile flipping or rotation are decoded using
    the Global Tile ID (GID) encoding defined in the Tiled Map Editor:
    - Horizontal flip: 0x80000000
    - Vertical flip: 0x40000000
    - Diagonal flip: 0x20000000
    - Rotated hex: 0x10000000

    Reference: https://doc.mapeditor.org/en/stable/reference/global-tile-ids/

    Each tile is represented as an `Actor` object with its properties and position
    set according to the decoded information.

    Examples:
        CSV file contents:
            1,2,3
            4,-1,5

        Function call:
            tiles = build("path/to/map.csv", 32, scale=2)

        Returns:
            A list of `Actor` objects corresponding to the tiles with their respective
            transformations applied.
    """
    with open(f"{DIR_PATH}/{csv_path}", "r") as f:
        contents = f.read().splitlines()

    # Convert CSV contents to a 2D list of integers, handling negative numbers
    contents = [
        [int(col) if col[0] != "-" else -int(col[1:])
         for col in row.split(",")]
        for row in contents
    ]

    # Create Actor objects for each tile
    items = []
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            tile_num = contents[row][col]
            if tile_num != -1:  # Ignore empty or invalid tiles
                # Decode flipping and rotation flags
                flipped_h = bool(tile_num & 0x80000000)
                flipped_v = bool(tile_num & 0x40000000)
                flipped_d = bool(tile_num & 0x20000000)
                rotated_hex = bool(tile_num & 0x10000000)
                tile_num &= 0x0FFFFFFF  # Remove flag bits to get the actual tile ID

                # Create an Actor for the tile
                item = Actor(f"tiles/tile_{tile_num:04d}")
                item.scale = scale
                if flipped_d:
                    item.flip_d = True
                if flipped_h:
                    item.flip_h = True
                if flipped_v:
                    item.flip_v = True
                if rotated_hex:
                    pass  # Reserved for additional transformations
                # Set the position of the tile
                item.topleft = (tile_size * col * scale,
                                tile_size * row * scale)
                items.append(item)

    return items


def pgz_map(
    csv_path,
    tilesheet_path,
    tile_set_size,
    tile_map_size=None,
    scale=1,
    spacing=0,
    margin=0,
):
    """
    Builds a list of Pygame Zero Actors from a tilesheet and a CSV tile map from Tiled.

    Args:
        filename (str): Path to the CSV file defining the tile map.
        tilesheet_path (str): Path to the tilesheet image.
        tile_set_size (int): Size of each tile in pixels from the tilesheet.
        tile_map_size (int): Desired size of each tile in the map (scaled size).
        scale (float): Global scale factor for the tiles.
        spacing (int): Number of pixels between tiles on the tilesheet.
        margin (int): Number of pixels around the border of the tilesheet.

    Returns:
        list: A list of Pygame Zero Actor objects representing the tile map.
    """
    # Load the tilesheet as a Pygame Surface
    tilesheet = pygame.image.load(f"{DIR_PATH}/{tilesheet_path}")

    # Calculate the number of tiles per row and column on the tilesheet
    tilesheet_width = (tilesheet.get_width() - 2 * margin + spacing) // (
        tile_set_size + spacing
    )
    tilesheet_height = (tilesheet.get_height() - 2 * margin + spacing) // (
        tile_set_size + spacing
    )

    # Determine the scaling factor for the tiles if tile_map_size is provided
    tile_scale = tile_map_size / tile_set_size if tile_map_size else 1

    with open(f"{DIR_PATH}/{csv_path}", "r") as f:
        contents = f.read().splitlines()

    # Convert to int but check for negative numbers
    contents = [
        [int(col) if col[0] != "-" else -int(col[1:])
         for col in row.split(",")]
        for row in contents
    ]

    # Create all items as Actors
    items = []
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            tile_num = contents[row][col]
            if tile_num != -1:
                # Decode any flags
                flipped_h = bool(tile_num & 0x80000000)
                flipped_v = bool(tile_num & 0x40000000)
                flipped_d = bool(tile_num & 0x20000000)
                rotated_hex = bool(tile_num & 0x10000000)
                tile_num &= 0x0FFFFFFF

                # Calculate the tile's position on the tilesheet
                tile_x = margin + (tile_num % tilesheet_width) * (
                    tile_set_size + spacing
                )
                tile_y = margin + (tile_num // tilesheet_width) * (
                    tile_set_size + spacing
                )

                # Crop the tile from the tilesheet
                tile_surface = tilesheet.subsurface(
                    (tile_x, tile_y, tile_set_size, tile_set_size)
                )

                # Scale the tile based on tile_scale
                new_size = (
                    int(tile_set_size * tile_scale),
                    int(tile_set_size * tile_scale),
                )
                tile_surface = pygame.transform.scale(tile_surface, new_size)

                # Create an Actor with the cropped and scaled tile
                item = Actor(tile_surface)
                item.scale = scale
                if flipped_h:
                    item.flip_h = True
                if flipped_v:
                    item.flip_v = True
                if flipped_d:
                    item.flip_d = True
                if rotated_hex:
                    pass

                # Adjust the position of the Actor based on the scaled map size
                item.topleft = (
                    (tile_map_size or tile_set_size) * col * scale,
                    (tile_map_size or tile_set_size) * row * scale,
                )
                items.append(item)

    return items


class Actor(Actor):
    """
    A class representing an actor in the game, which can be rendered on the screen
    and supports image transformations such as scaling, flipping, and rotating.

    Attributes:
        flip_h (bool): Whether the actor's image is flipped horizontally.
        flip_v (bool): Whether the actor's image is flipped vertically.
        flip_d (bool): Whether the actor's image is flipped diagonally (rotated 90° and flipped).
        scale (float): Scaling factor for the actor's image.
        fps (int): Frames per second for animation.
        direction (int): Directional property of the actor.
        image (str or pygame.Surface): Image used for the actor, as a path or surface.
        sprite (Sprite): Sprite object associated with the actor.
        angle (float): Rotation angle of the actor's image in degrees.
    """

    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        """
        Initializes the actor with an image, position, and optional transformations.

        Args:
            image (str or pygame.Surface): Path to the image file or a preloaded pygame.Surface.
            pos (tuple, optional): Position of the actor. Defaults to `POS_TOPLEFT`.
            anchor (tuple, optional): Anchor point for positioning. Defaults to `ANCHOR_CENTER`.
            **kwargs: Additional arguments for the base Actor class.
        """
        self._flip_h = False
        self._flip_v = False
        self._flip_d = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5
        self.direction = 0
        self._image_name = None
        self._orig_surf = None
        self._surf = None

        if isinstance(image, pygame.Surface):
            self._orig_surf = self._surf = image
        else:
            self._image_name = image
            self._orig_surf = self._surf = loaders.images.load(image)

        super().__init__(image, pos, anchor, **kwargs)

    @property
    def images(self):
        """list: The list of images for animation."""
        return self._images

    @images.setter
    def images(self, images):
        """Sets the list of images for animation."""
        self._images = images
        if len(self._images) != 0:
            self.image = self._images[0]

    def next_image(self):
        """
        Advances to the next image in the animation sequence.
        Loops back to the first image after the last one.
        """
        if self.image in self._images:
            current = self._images.index(self.image)
            if current == len(self._images) - 1:
                self.image = self._images[0]
            else:
                self.image = self._images[current + 1]
        else:
            self.image = self._images[0]

    def animate(self):
        """
        Animates the actor by advancing the image based on time and FPS.
        Updates the frame only if enough time has passed since the last frame change.
        """
        now = int(time.time() * self.fps)
        if now != self._animate_counter:
            self._animate_counter = now
            self.next_image()

    @property
    def scale(self):
        """float: Scaling factor for the actor's image."""
        return self._scale

    @scale.setter
    def scale(self, scale):
        """Sets the scaling factor and applies the transformation."""
        self._scale = scale
        self._transform_surf()

    @property
    def flip_h(self):
        """bool: Whether the actor's image is flipped horizontally."""
        return self._flip_h

    @flip_h.setter
    def flip_h(self, flip_h):
        """Sets horizontal flipping and applies the transformation."""
        self._flip_h = flip_h
        self._transform_surf()

    @property
    def flip_v(self):
        """bool: Whether the actor's image is flipped vertically."""
        return self._flip_v

    @flip_v.setter
    def flip_v(self, flip_v):
        """Sets vertical flipping and applies the transformation."""
        self._flip_v = flip_v
        self._transform_surf()

    @property
    def flip_d(self):
        """bool: Whether the actor's image is flipped diagonally."""
        return self._flip_d

    @flip_d.setter
    def flip_d(self, flip_d):
        """Sets diagonal flipping and applies the transformation."""
        self._flip_d = flip_d
        self._transform_surf()

    @property
    def sprite(self):
        """Sprite: The sprite associated with the actor."""
        return self._sprite

    @sprite.setter
    def sprite(self, sprite):
        """Sets the sprite associated with the actor."""
        self._sprite = sprite

    @property
    def image(self):
        """str or pygame.Surface: The image used by the actor."""
        return self._image_name

    @image.setter
    def image(self, image):
        """
        Sets the actor's image, either as a surface or by loading from a path.

        Args:
            image (str or pygame.Surface): Image path or preloaded surface.
        """
        if isinstance(image, pygame.Surface):
            self._orig_surf = self._surf = image
            self._image_name = None
        else:
            self._image_name = image
            self._orig_surf = self._surf = loaders.images.load(image)
        self._update_pos()
        self._transform_surf()

    @property
    def angle(self):
        """float: Rotation angle of the actor's image in degrees."""
        return self._angle

    @angle.setter
    def angle(self, value):
        """Sets the rotation angle and applies the transformation."""
        if self._angle != value:
            self._angle = value
            self._transform_surf()

    def _transform_surf(self):
        """
        Applies transformations (scaling, flipping, rotation) to the actor's image.
        Adjusts the anchor and dimensions to match the transformed image.
        """
        self._surf = self._orig_surf
        p = self.pos

        if self._scale != 1:
            size = self._orig_surf.get_size()
            self._surf = pygame.transform.scale(
                self._surf, (int(size[0] * self.scale),
                             int(size[1] * self.scale))
            )

        if self._flip_h:
            self._surf = pygame.transform.flip(self._surf, True, False)
        if self._flip_v:
            self._surf = pygame.transform.flip(self._surf, False, True)
        if self._flip_d and not self._flip_h:
            self._surf = pygame.transform.rotate(self._surf, -90)
            self._surf = pygame.transform.flip(self._surf, True, False)
        if self._flip_d and self._flip_h:
            self._surf = pygame.transform.rotate(self._surf, 90)
            self._surf = pygame.transform.flip(self._surf, True, False)

        if self._angle != 0:
            self._surf = pygame.transform.rotate(self._surf, self._angle)

        self.width, self.height = self._surf.get_size()
        w, h = self._orig_surf.get_size()
        ax, ay = self._untransformed_anchor
        anchor = transform_anchor(ax, ay, w, h, self._angle)
        self._anchor = (anchor[0] * self.scale, anchor[1] * self.scale)

        self.pos = p
        self._mask = None

    def draw(self):
        """
        Draws the actor on the screen using its current transformed image.
        """
        game.screen.blit(self._surf, self._rect.topleft)


class SpriteSheet(object):
    """
    A utility class for handling sprite sheets, allowing extraction of individual
    images or strips of images for use in animations and games.

    Attributes:
        sheet (pygame.Surface): The loaded sprite sheet image.
    """

    def __init__(self, filename):
        """
        Initializes the SpriteSheet by loading an image file.

        Args:
            filename (str): Path to the sprite sheet image file.

        Raises:
            pygame.error: If the image cannot be loaded.
        """
        try:
            self.sheet = pygame.image.load(filename)
        except pygame.error as message:
            print(f"Unable to load sprite sheet image: {message}")

    def image_at(self, rectangle, color_key=None):
        """
        Extracts a single image from the sprite sheet.

        Args:
            rectangle (tuple): The (x, y, width, height) of the image on the sprite sheet.
            color_key (tuple or int, optional): Color key for transparency.
                If -1, the top-left pixel of the image will be used as the color key.
                Defaults to None, meaning no transparency.

        Returns:
            pygame.Surface: The extracted image.
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    def images_at(self, rects, color_key=None):
        """
        Extracts multiple images from the sprite sheet.

        Args:
            rects (list of tuples): A list of (x, y, width, height) rectangles defining the images.
            color_key (tuple or int, optional): Color key for transparency.
                If -1, the top-left pixel of each image will be used as the color key.
                Defaults to None, meaning no transparency.

        Returns:
            list of pygame.Surface: The extracted images.
        """
        return [self.image_at(rect, color_key) for rect in rects]

    def load_strip(self, rect, image_count, color_key=None):
        """
        Extracts a strip of sequential images from the sprite sheet.

        Args:
            rect (tuple): The (x, y, width, height) rectangle of the first image in the strip.
            image_count (int): The number of images in the strip.
            color_key (tuple or int, optional): Color key for transparency.
                If -1, the top-left pixel of each image will be used as the color key.
                Defaults to None, meaning no transparency.

        Returns:
            list of pygame.Surface: The extracted images in the strip.
        """
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, color_key)


class Sprite(object):
    def __init__(
        self,
        image_filename,
        frame_width,
        frame_height,
        row_number,
        frame_count,
        fps=10,
        transparent_color=(0, 0, 0),
    ):
        """
        A class representing a sprite with multiple frames for animation.

        Args:
            image_filename (str): The name of the sprite sheet image file.
            frame_width (int): The width of each frame in the sprite sheet.
            frame_height (int): The height of each frame in the sprite sheet.
            row_number (int): The row number (starting from 0) from which the frames will be extracted.
            frame_count (int): The number of frames in the animation.
            fps (int, optional): The number of frames per second for the animation. Defaults to 10.
            transparent_color (tuple, optional): RGB color key for transparency. Defaults to (0, 0, 0).
        """
        self.filename = image_filename
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.row_number = row_number
        self.frame_count = frame_count
        self.fps = fps
        self.last_update_time = pygame.time.get_ticks()  # Track time in milliseconds
        ss = SpriteSheet(f"{DIR_PATH}/images/sprites/{image_filename}")
        # self.images = ss.load_strip(rect, count, color_key)

        # Load sprite sheet and extract frames
        # ss = SpriteSheet(f"{DIR_PATH}/images/sprites/{image_filename}")
        # self.images = self._extract_frames(ss)
        frame_rect = (0, frame_height * row_number, frame_width, frame_height)
        self.images = ss.load_strip(frame_rect, frame_count, transparent_color)

        self.i = 0  # Current frame index

    def _extract_frames(self, sprite_sheet):
        """
        Extracts frames from the sprite sheet based on the specified row number.

        Returns:
            list: A list of `pygame.Surface` objects representing the frames.
        """
        frames = []
        x_offset = 0  # Start at the left edge of the sprite sheet
        y_offset = (
            self.row_number * self.frame_height
        )  # Calculate the y position based on the row number

        for frame_index in range(self.frame_count):
            # Calculate the (x, y) position for each frame in the sprite sheet
            x = x_offset + (frame_index * self.frame_width)
            y = y_offset

            # Define the rectangle area for each frame
            frame_rect = (x, y, self.frame_width, self.frame_height)

            # Use the get_surface method to get the frame
            frame = sprite_sheet.get_surface(
                frame_rect
            )  # Adjust method name accordingly
            frames.append(frame)

        return frames  # Return the requested frames

    def next(self):
        """
        Advances to the next frame in the sprite animation based on time elapsed.

        Returns:
            pygame.Surface: The next image in the sprite animation.
        """
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        frame_duration_ms = 1000 / self.fps  # Duration for each frame in milliseconds

        # Update frame if enough time has passed
        if current_time - self.last_update_time >= frame_duration_ms:
            self.i = (self.i + 1) % len(
                self.images
            )  # Loop back to the first frame if necessary
            self.last_update_time = current_time  # Reset the last update time

        return self.images[self.i]


class SpriteActor(Actor):
    def __init__(
        self,
        sprite_instance,
        position=POS_TOPLEFT,
        anchor_point=ANCHOR_CENTER,
        **kwargs,
    ):
        """
        An actor that uses a sprite for animation.

        Args:
            sprite_instance (Sprite): The sprite instance to use for animation.
            position (tuple, optional): Initial position of the actor. Defaults to `POS_TOPLEFT`.
            anchor_point (tuple, optional): Anchor point of the actor. Defaults to `ANCHOR_CENTER`.
            **kwargs: Additional arguments for the base Actor class.
        """
        self._flip_h = False
        self._flip_v = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5  # Target frames per second
        self.direction = 0
        self.sprite = sprite_instance
        self._last_frame_time = (
            pygame.time.get_ticks()
        )  # Track last update time in milliseconds
        super().__init__(
            f"sprites/{sprite_instance.filename}", position, anchor_point, **kwargs
        )
        self._orig_surf = self.sprite.images[self.sprite.i]
        self._update_pos()
        self._transform_surf()

    @property
    def sprite(self):
        """The sprite instance associated with the actor."""
        return self._sprite

    @sprite.setter
    def sprite(self, sprite_instance):
        """
        Sets the sprite instance for the actor.

        Args:
            sprite_instance (Sprite): The new sprite instance.
        """
        self._sprite = sprite_instance

    def draw(self):
        """
        Draws the sprite actor to the screen, updating its animation based on the current time.
        """
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        # Update sprite's frame based on elapsed time
        self._orig_surf = self.sprite.next()
        self._update_pos()
        self._transform_surf()
        game.screen.blit(self._surf, self.topleft)
