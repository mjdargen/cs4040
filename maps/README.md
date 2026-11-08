# Maps and tilesets — sources and credits

This directory contains maps and tilesets for [Tiled Map Editor](https://www.mapeditor.org/), used by the Pygame Zero Plus tilemap examples:

- `.tmx` — tilemaps and level layouts.
- `.tsx` — tileset definitions that refer to images.
- `.png` — tileset graphics.

Keep the `.tmx`, `.tsx`, and referenced `.png` files together so paths inside Tiled maps remain valid.

After adding or changing maps or tilesets, run `python utils/map_and_sprite_checker.py` from the repository folder to check that everything loads in Pygame Zero Plus.

## Naming

Every tileset is a matching `.png` and `.tsx` pair named

```
<style>_<theme>_<author>
```

- **style** is `platformer` (side view, with gravity) or `topdown` (seen from above, like an RPG).
- **theme** names the asset pack. Each pack is one tileset: all of its sheets are packed into a single image, with duplicate sheets removed.
- **author** is the artist to credit. It tells you which entry in [Asset credits](#asset-credits) to cite.

To use a tileset in Tiled, choose **Map > Add External Tileset...** and pick its `.tsx` file. Set the map's tile size to match the tileset's (the **Tile size** column below), and don't mix tile sizes within one map.

## Platformer tilesets

Kenney: `platformer_1bit_kenney` (16×16), `platformer_abstract_kenney` (64×64), `platformer_farm_kenney` (18×18), `platformer_food_kenney` (18×18), `platformer_industrial_kenney` (18×18), `platformer_new_kenney` (64×64), `platformer_pico8_kenney` (8×8), `platformer_pixel_kenney` (18×18)

| Tileset | Tile size | Grid (columns × rows) | Contents | Source pack |
|---|---|---|---|---|
| `platformer_fourseasons_rottingpixels` | 16x16 | 16 × 16 | Ground blocks in four seasonal palettes, ? and ! blocks, trees, mushrooms, ladders, signs, water and lava | [Four Seasons Platformer Tileset](https://rottingpixels.itch.io/four-seasons-platformer-tileset-16x16free) |
| `platformer_grassland_shackhal` | 16x16 | 16 × 17 | Whole GrassLand set: 47-tile grass terrain, background cave walls, floating islands, bridges, water, a large tree, bushes, rocks, flowers, cave doorways | [Multi Platformer Tileset](https://shackhal.itch.io/multi-platformer-tileset) |

## Top-down tilesets

Kenney: `topdown_dungeon_kenney` (16×16), `topdown_factory_kenney` (16×16), `topdown_farm_kenney` (16×16), `topdown_pico8_kenney` (8×8), `topdown_ski_kenney` (16×16), `topdown_town_kenney` (16×16)

| Tileset | Tile size | Grid (columns × rows) | Contents | Source pack |
|---|---|---|---|---|
| `topdown_ninja_pixelboy` | 16x16 | 80 × 107 | Whole Ninja Adventure tileset collection (22 sheets): ground and paths, water and shores, cliffs, holes, desert, abandoned village, houses and shops, towers, trees and rocks, camp, furniture, beds, indoor walls and floors, dungeon puzzle objects, pipes, and colored logic markers | [Ninja Adventure](https://pixel-boy.itch.io/ninja-adventure-asset-pack) |

## Asset credits

All of the art in this folder may be shared and reused, including in commercial projects. Attribution is not required, but please credit the artist when you use their art, for example: *"Tileset: Ninja Adventure Asset Pack by Pixel-Boy and AAA (CC0)"*.

- **[Kenney](https://kenney.nl/assets)** — tilesets ending in `_kenney`. Released under **[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)**.
- **Pixel-Boy and AAA** — `topdown_ninja_pixelboy`, from the [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack). Released under **[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)**.
- **Shackhal (Diego "Shackhal" del Solar)** — `platformer_grassland_shackhal`, from the free GrassLand version of the [Multi Platformer Tileset](https://shackhal.itch.io/multi-platformer-tileset). Released under **[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)**.
- **RottingPixels** — `platformer_fourseasons_rottingpixels`, from the [Four Seasons Platformer Tileset](https://rottingpixels.itch.io/four-seasons-platformer-tileset-16x16free) as repackaged in the [Brackeys Platformer Bundle](https://brackeysgames.itch.io/brackeys-platformer-bundle), which Brackeys releases under **[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)**. The artist's own page allows use in free and commercial projects and modification; credit is appreciated.
- **[Tiled Map Editor](https://www.mapeditor.org/)** — the editor and file format used for the `.tmx` and `.tsx` files. Tiled is a tool, not the art creator.

### More free tilesets you can download yourself

These packs are free to download, but their licenses don't allow them to be re-shared here, so they aren't included. To use one, download it from the artist's page and follow that page's license. Several allow only non-commercial use.

| Pack | Artist | Style | Credit |
|---|---|---|---|
| [Cute Fantasy RPG (Free)](https://kenmi-art.itch.io/cute-fantasy-rpg) | Kenmi | Top-down | Requested |
| [Tiny Farm RPG Asset Pack](https://maevedevs.itch.io/farm-rpg) | Maeve Devs | Top-down | Appreciated |
| [Modern Interiors (Free)](https://limezu.itch.io/moderninteriors) | LimeZu | Top-down | Required |
| [Pixel Art Top Down - Basic](https://cainos.itch.io/pixel-art-top-down-basic) | Cainos | Top-down | Appreciated |
| [Sprout Lands Basic Pack](https://cupnooble.itch.io/sprout-lands-asset-pack) | Cup Nooble | Top-down | Required |
| [The Fan-tasy Tileset (Free)](https://ventilatore.itch.io/the-fantasy-tileset) | Ventilatore | Top-down | Appreciated |
| [Tiny Swords (Free)](https://pixelfrog-assets.itch.io/tiny-swords) | Pixel Frog | Top-down | Not required |
| [Legacy Fantasy - High Forest](https://anokolisa.itch.io/sidescroller-pixelart-sprites-asset-pack-forest-16x16) | Anokolisa | Platformer | Not required |
| [Mossy Cavern](https://maaot.itch.io/mossy-cavern) | Maaot | Platformer | Not required |
| [Free Swamp Game Tileset](https://craftpix.net/freebies/free-swamp-game-tileset-pixel-art/) | CraftPix.net | Platformer | Not required |
