# CS4040 — Game Design

Python game development examples and supporting assets for **CS4040 Game Design**, an introductory computer science course. The programs are designed to accompany class lessons and give students a starting point for experimenting with graphics, input, animation, game mechanics, and larger projects.

The examples use **[Pygame Zero Plus](https://github.com/mjdargen/pgzero)**, an independently maintained fork of [Pygame Zero](https://github.com/lordmauve/pgzero) with additional features for teaching and developing 2D games.

## Getting started

1. Install [Pygame Zero Plus](https://github.com/mjdargen/pgzero#installation) using the instructions in the framework repository.
2. Clone this repository and open it in your Python editor (such as VS Code):

   ```bash
   git clone https://github.com/mjdargen/cs4040.git
   cd cs4040
   ```

3. Open and run an example using your editor's Run button or `python <filename>.py` from the repository root.

Keep the asset directories next to the example programs so Pygame Zero Plus can find their images, sprites, sounds, and music. Many of the examples begin with `import pgzrun` and `from pgzero.builtins import *` and end with `pgzrun.go()`; the explicit built-ins import also helps Python editors recognize Pygame Zero names.

## Assets and credits

These files are a mix of teaching assets and third-party resources. **The code repository and the media assets do not all share one license.** Each asset directory has a README describing known sources and any attribution or license details that still need verification.

| Directory                     | Contents and attribution                                                                                          |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [fonts/](fonts/README.md)     | Pixel and monospaced fonts; individual credits and license notes                                                  |
| [images/](images/README.md)   | Static sprites, characters, backgrounds, and other images                                                         |
| [maps/](maps/README.md)       | Tiled maps, tilesets, and map graphics                                                                            |
| [music/](music/README.md)     | Background music; **includes third-party game soundtrack arrangements with unverified redistribution permission** |
| [sounds/](sounds/README.md)   | Sound effects and source/licensing notes                                                                          |
| [sprites/](sprites/README.md) | Animated sprite sheets, editable source files, and per-sprite animation documentation                             |

Please follow each original creator's licensing terms before reusing or redistributing assets in your own projects.

## Framework

This repository contains examples and assets, not the underlying framework. For source code, installation, and framework documentation, see **[Pygame Zero Plus](https://github.com/mjdargen/pgzero)**.
