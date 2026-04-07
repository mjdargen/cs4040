import os
import pygame
import xml.etree.ElementTree as ET

from . import loaders
from .actor import Actor


FLIP_H = 0x80000000
FLIP_V = 0x40000000
FLIP_D = 0x20000000
GID_MASK = 0x0FFFFFFF


def _load_xml_from_maps(name):
    text = loaders.maps.load(name)
    return ET.fromstring(text)


def _resolve_relative_map_path(base_name, relative_path):
    base_dir = os.path.dirname(base_name)
    if base_dir:
        return os.path.normpath(os.path.join(base_dir, relative_path)).replace(
            "\\", "/"
        )
    return relative_path


def _load_tilesets(root, tmx_name):
    tilesets = {}

    for ts in root.findall("tileset"):
        firstgid = int(ts.attrib["firstgid"])

        if "source" in ts.attrib:
            tsx_name = _resolve_relative_map_path(tmx_name, ts.attrib["source"])
            ts_root = _load_xml_from_maps(tsx_name)
        else:
            ts_root = ts

        image = ts_root.find("image")
        if image is None:
            raise ValueError("Tileset is missing an <image> tag")

        image_name = _resolve_relative_map_path(
            os.path.dirname(tmx_name) if "/" in tmx_name else "",
            image.attrib["source"],
        )
        tilesheet = loaders.mapimages.load(image_name)

        tile_width = int(ts_root.attrib["tilewidth"])
        tile_height = int(ts_root.attrib["tileheight"])
        spacing = int(ts_root.attrib.get("spacing", 0))
        margin = int(ts_root.attrib.get("margin", 0))

        sheet_w = (tilesheet.get_width() - 2 * margin + spacing) // (
            tile_width + spacing
        )
        sheet_h = (tilesheet.get_height() - 2 * margin + spacing) // (
            tile_height + spacing
        )

        tilesets[firstgid] = {
            "image": tilesheet,
            "tile_width": tile_width,
            "tile_height": tile_height,
            "sheet_w": sheet_w,
            "sheet_h": sheet_h,
            "spacing": spacing,
            "margin": margin,
        }

    return tilesets


def load_tile_map_actors(tmx_name, scale=1):
    """
    Load a Tiled TMX map into a dict of:
        {layer_name: [Actor, Actor, ...]}

    The TMX/TSX/image files are loaded through pgzero loaders from the maps folder.
    """
    root = _load_xml_from_maps(tmx_name)

    map_tile_width = int(root.attrib["tilewidth"])
    map_tile_height = int(root.attrib["tileheight"])

    tilesets = _load_tilesets(root, tmx_name)

    layers_dict = {}

    for layer in root.findall("layer"):
        name = layer.attrib["name"]
        width = int(layer.attrib["width"])
        height = int(layer.attrib["height"])
        data = layer.find("data")

        if data is None or data.text is None:
            layers_dict[name] = []
            continue

        encoding = data.attrib.get("encoding")
        if encoding != "csv":
            raise ValueError(
                f"Layer '{name}' must use CSV encoding. Found: {encoding!r}"
            )

        contents = [
            [int(v) for v in row.split(",") if v.strip()]
            for row in data.text.strip().splitlines()
        ]

        items = []

        for row in range(height):
            for col in range(width):
                tile_gid = contents[row][col]
                if tile_gid == 0:
                    continue

                flipped_h = bool(tile_gid & FLIP_H)
                flipped_v = bool(tile_gid & FLIP_V)
                flipped_d = bool(tile_gid & FLIP_D)
                tile_gid &= GID_MASK

                ts_firstgid = max(gid for gid in tilesets if gid <= tile_gid)
                tileset = tilesets[ts_firstgid]
                local_id = tile_gid - ts_firstgid

                tx = tileset["margin"] + (local_id % tileset["sheet_w"]) * (
                    tileset["tile_width"] + tileset["spacing"]
                )
                ty = tileset["margin"] + (local_id // tileset["sheet_w"]) * (
                    tileset["tile_height"] + tileset["spacing"]
                )

                tile_surface = (
                    tileset["image"]
                    .subsurface(
                        (tx, ty, tileset["tile_width"], tileset["tile_height"])
                    )
                    .copy()
                )

                tile_scale_x = map_tile_width / tileset["tile_width"]
                tile_scale_y = map_tile_height / tileset["tile_height"]

                scaled_size = (
                    int(round(tileset["tile_width"] * tile_scale_x)),
                    int(round(tileset["tile_height"] * tile_scale_y)),
                )
                tile_surface = pygame.transform.scale(tile_surface, scaled_size)

                actor = Actor(tile_surface)
                actor.scale = scale
                actor.flip_h = flipped_h
                actor.flip_v = flipped_v
                actor.flip_d = flipped_d
                actor.topleft = (
                    map_tile_width * col * scale,
                    map_tile_height * row * scale,
                )

                items.append(actor)

        layers_dict[name] = items

    return layers_dict
