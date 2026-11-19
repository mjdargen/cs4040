# Maps and tilesets

This directory contains maps and tilesets for [Tiled Map Editor](https://www.mapeditor.org/), used by the Pygame Zero Plus tilemap examples:

- `.tmx` — tilemaps and level layouts.
- `.tsx` — tileset definitions that refer to images.
- `.png` — tileset graphics.

Keep the `.tmx`, `.tsx`, and referenced `.png` files together so paths inside Tiled maps remain valid.

After adding or changing maps or tilesets, run `python utils/map_and_sprite_checker.py` from the repository folder to check that everything loads in Pygame Zero Plus.

All of the art in the tables below is released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), so it may be shared and reused, including in commercial projects. The exception is the `_kevinsmomshouse` tilesets: their designer gives no license, but lets anyone use them in their own projects, with credit appreciated but not necessary. Attribution is not required, but please credit the designer when you use their art, for example: *"Tileset: Ninja Adventure Asset Pack by Pixel-Boy and AAA (CC0)"*.

## Naming

Every tileset is a matching `.png` and `.tsx` pair named

```
<style>_<theme>_<author>
```

- **style** is `platformer` (side view, with gravity) or `topdown` (seen from above, like an RPG).
- **theme** names the asset pack. Each pack is one tileset: all of its sheets are packed into a single image, with duplicate sheets removed.
- **author** is the designer to credit (the **Designer** column below).

To use a tileset in Tiled, choose **Map > Add External Tileset...** and pick its `.tsx` file. Set the map's tile size to match the tileset's (the **Tile size** column below), and don't mix tile sizes within one map.

## Top-down tilesets

| Asset | Description | Tile size | Grid (cols × rows) | Image size | Designer | Source |
|---|---|---|---|---|---|---|
| `topdown_city_kenney` | Modern city: roads, sidewalks, brick and concrete buildings, trees, signs, people, and cars | 16 × 16 | 12 × 11 | 192 × 176 | Kenney | [Tiny City](https://kenney.nl/assets/tiny-city) |
| `topdown_dungeon_kenney` | Dungeon: stone walls and floors, doors, chests, heroes, monsters, weapons, and potions | 16 × 16 | 12 × 11 | 192 × 176 | Kenney | [Tiny Dungeon](https://kenney.nl/assets/tiny-dungeon) |
| `topdown_factory_kenney` | Factory: conveyor belts, pipes, machines, crates, and floor tiles | 16 × 16 | 12 × 11 | 192 × 176 | Kenney | [Tiny Factory](https://kenney.nl/assets/tiny-factory) |
| `topdown_farm_kenney` | Farm: tilled soil, crops, trees, fences, barns, tools, and animals | 16 × 16 | 12 × 11 | 192 × 176 | Kenney | [Tiny Farm](https://kenney.nl/assets/tiny-farm) |
| `topdown_ninja_pixelboy` | The whole Ninja Adventure tileset collection (22 sheets): ground, water, cliffs, desert, villages, houses, trees, interiors, and dungeon puzzle objects | 16 × 16 | 80 × 107 | 1280 × 1712 | Pixel-Boy and AAA | [Ninja Adventure Asset Pack](https://pixel-boy.itch.io/ninja-adventure-asset-pack) |
| `topdown_pico8_kenney` | PICO-8 palette city: roads, buildings, roofs, trees, and vehicles | 8 × 8 | 24 × 15 | 192 × 120 | Kenney | [Pico-8 City](https://kenney.nl/assets/pico-8-city) |
| `topdown_ski_kenney` | Ski slope: snow, trees, flags, ski lift, skiers, and a font | 16 × 16 | 12 × 11 | 192 × 176 | Kenney | [Tiny Ski](https://kenney.nl/assets/tiny-ski) |
| `topdown_town_kenney` | Medieval town: grass, paths, trees, houses, castle walls, fences, and items | 16 × 16 | 12 × 11 | 192 × 176 | Kenney | [Tiny Town](https://kenney.nl/assets/tiny-town) |

## Platformer tilesets

| Asset | Description | Tile size | Grid (cols × rows) | Image size | Designer | Source |
|---|---|---|---|---|---|---|
| `platformer_1bit_kenney` | Black-and-white 1-bit: platforms, ladders, spikes, machines, characters, and enemies | 16 × 16 | 20 × 20 | 320 × 320 | Kenney | [1-Bit Platformer Pack](https://kenney.nl/assets/1-bit-platformer-pack) |
| `platformer_abstract_kenney` | Flat-colored ground in four color sets with slopes, plants, keys, locks, doors, levers, and signs. `platformer_abstract_kenney_slopes.tsx` uses the same image with slope heights set on the ramp tiles | 64 × 64 | 22 × 12 | 1408 × 768 | Kenney | [Abstract Platformer](https://kenney.nl/assets/abstract-platformer) |
| `platformer_farm_kenney` | Farm expansion for Pixel Platformer: dirt, crops, greenhouses, fences, and tools | 18 × 18 | 16 × 7 | 288 × 126 | Kenney | [Pixel Platformer Farm Expansion](https://kenney.nl/assets/pixel-platformer-farm-expansion) |
| `platformer_food_kenney` | Food expansion for Pixel Platformer: cake and cookie terrain, candy, drinks, and snacks | 18 × 18 | 16 × 7 | 288 × 126 | Kenney | [Pixel Platformer Food Expansion](https://kenney.nl/assets/pixel-platformer-food-expansion) |
| `platformer_fourseasons_rottingpixels` | Ground blocks in four seasonal palettes, ? and ! blocks, trees, mushrooms, ladders, signs, water, and lava | 16 × 16 | 16 × 16 | 256 × 256 | RottingPixels | [Four Seasons Platformer Tileset](https://rottingpixels.itch.io/four-seasons-platformer-tileset-16x16free) (CC0 via the [Brackeys Platformer Bundle](https://brackeysgames.itch.io/brackeys-platformer-bundle)) |
| `platformer_grassland_shackhal` | The whole GrassLand set: grass terrain, cave walls, floating islands, bridges, water, a large tree, bushes, rocks, and cave doorways | 16 × 16 | 16 × 17 | 256 × 272 | Shackhal | [Multi Platformer Tileset](https://shackhal.itch.io/multi-platformer-tileset) (free GrassLand version) |
| `platformer_industrial_kenney` | Industrial expansion for Pixel Platformer: metal platforms, girders, pipes, chains, and hazard signs | 18 × 18 | 16 × 7 | 288 × 126 | Kenney | [Pixel Platformer Industrial Expansion](https://kenney.nl/assets/pixel-platformer-industrial-expansion) |
| `platformer_jungle_kevinsmomshouse` | Jungle: mossy ground with slopes and dripping cave ceilings, hanging vines, grass, jungle trees and canopy, and water and waterfalls | 8 × 8 | 19 × 19 | 152 × 152 | Kevin's Mom's House | [Jungle pico-platformer tileset](https://kevins-moms-house.itch.io/jungle-pico-platformer-tileset) |
| `platformer_mesa_kevinsmomshouse` | Desert mesa: orange and striped rock ground in several shades with slopes and cave ceilings, cavern walls, cacti, dead trees, and water and waterfalls | 8 × 8 | 29 × 48 | 232 × 384 | Kevin's Mom's House | [Mesa pico-platformer tileset](https://kevins-moms-house.itch.io/mesa-pico-platformer-tileset) |
| `platformer_new_kenney` | Grass, dirt, sand, stone, snow, and purple terrain with slopes, plus blocks, coins, gems, keys, locks, flags, springs, and enemies. 1 px spacing between tiles | 64 × 64 | 18 × 18 | 1169 × 1169 | Kenney | [New Platformer Pack](https://kenney.nl/assets/new-platformer-pack) |
| `platformer_pico8_kenney` | PICO-8 palette platformer: terrain, characters, items, and numbers | 8 × 8 | 15 × 10 | 120 × 80 | Kenney | [Pico-8 Platformer](https://kenney.nl/assets/pico-8-platformer) |
| `platformer_pixel_kenney` | Grass, dirt, and snow terrain, blocks, ladders, water, pipes, trees, coins, hearts, and numbers | 18 × 18 | 20 × 9 | 360 × 162 | Kenney | [Pixel Platformer](https://kenney.nl/assets/pixel-platformer) |
| `platformer_ruins_kevinsmomshouse` | Ruins: stone and mossy stone ground with slopes and cave ceilings, vines, temple walls with torches and pillars, doors and gates, traps, and two kinds of water | 8 × 8 | 34 × 36 | 272 × 288 | Kevin's Mom's House | [Ruin pico-platformer tileset](https://kevins-moms-house.itch.io/ruin-pico-platformer-tileset) |
| `platformer_savanna_kevinsmomshouse` | Savanna: sandy ground with slopes and cave ceilings, cavern walls, grass, acacia trees, and water and waterfalls | 8 × 8 | 17 × 18 | 136 × 144 | Kevin's Mom's House | [Savanna pico-platformer tileset](https://kevins-moms-house.itch.io/savanna-pico-platformer-tileset) |
| `platformer_swamp_kevinsmomshouse` | Swamp: mossy ground with slopes and cave ceilings, vines, a swamp tree, mushrooms, and water and waterfalls | 8 × 8 | 19 × 12 | 152 × 96 | Kevin's Mom's House | [Swamp pico-platformer tileset](https://kevins-moms-house.itch.io/swamp-pico-platformer-tileset) |
| `platformer_tropicalocean_kevinsmomshouse` | Tropical island and seabed: sandy ground with slopes and cave ceilings, grass, palm trees, underwater sand with seaweed and coral, and water | 8 × 8 | 27 × 17 | 216 × 136 | Kevin's Mom's House | [Tropical ocean pico-platformer tileset](https://kevins-moms-house.itch.io/tropical-ocean-pico-platformer-tileset) |
