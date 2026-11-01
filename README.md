# CS4040 — Game Design

Python game development examples and supporting assets for **CS4040 Game Design**, an introductory computer science course. The programs are designed to accompany class lessons and give students a starting point for experimenting with graphics, input, animation, game mechanics, and larger projects.

The examples use **[Pygame Zero Plus](https://github.com/mjdargen/pgzero)**, an independently maintained fork of [Pygame Zero](https://github.com/lordmauve/pgzero) with additional features for teaching and developing 2D games.

## Getting started

1. Install Pygame Zero Plus. It also installs pygame and numpy.

   **Windows:**

   ```bash
   python -m pip install --upgrade --pre pgzero-plus
   ```

   **macOS / Linux:**

   ```bash
   python3 -m pip install --upgrade --pre pgzero-plus
   ```

   `--pre` includes alpha and beta releases. If you have installed the original Pygame Zero (`pgzero`) or pygame before, see [switching to Pygame Zero Plus](https://github.com/mjdargen/pgzero#switching-from-pygame-zero-pygame-or-an-older-fork) first.

2. Clone this repository and open it in your Python editor (such as VS Code):

   ```bash
   git clone https://github.com/mjdargen/cs4040.git
   cd cs4040
   ```

3. Open and run an example using your editor's Run button or `python <filename>.py` from the repository root.

To install everything this repository uses, including the packages for the utilities below, run `python -m pip install -r requirements.txt` from the repository root instead of step 1.

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

## Utilities

The [utils/](utils/) folder has scripts for preparing game assets:

| Script                    | What it does                                                                  |
| ------------------------- | ----------------------------------------------------------------------------- |
| `spritesheet_creator.py`  | Combines PNG and GIF animations into one sprite sheet, with documentation     |
| `spritesheet_packer.py`   | Stacks PNG animation strips into a sprite sheet, one strip per row            |
| `spritesheet_cropper.py`  | Removes padding around the frames of a sprite sheet                           |
| `piskel_unpacker.py`      | Exports frames from Piskel files                                              |
| `sprite_documenter.py`    | Writes documentation for Aseprite sprite files                                |
| `tile_packer.py`          | Removes the margins around each tile of a tileset or sprite sheet             |
| `resolve_tilemaps.py`     | Moves Tiled maps and tilesets into `maps/` and fixes the paths between them   |
| `convert_audio.py`        | Converts WAV and MP3 files to OGG                                             |
| `lowercase_filenames.py`  | Renames asset files to lowercase names that Pygame Zero Plus can load         |
| `convert_line_endings.py` | Converts text files to Linux line endings                                     |
| `update.py`               | Sets up a workspace with Pygame Zero Plus and this repository's games         |

`update.py` is for setting up a separate folder to work in. Copy it into that folder and run it there: `python update.py pygame` installs Pygame Zero Plus, and `python update.py all` copies in the examples and assets (use `python3` on macOS and Linux). Run it with no options to see everything it can do. It works on Windows, macOS and Linux with Python 3.6 or newer, and needs nothing else installed, not even git.

The other utilities need Python 3.7 or newer and [Pillow](https://pypi.org/project/pillow/), which `requirements.txt` installs. A few also need other programs:

- `convert_audio.py` needs [ffmpeg](https://ffmpeg.org/).
- `sprite_documenter.py` needs [Aseprite](https://www.aseprite.org/) and its command-line tool.
- The scripts with windows (`spritesheet_creator.py`, `spritesheet_packer.py` and `spritesheet_cropper.py`) use tkinter, which comes with Python on Windows and macOS. On Linux, install it with your package manager, e.g. `sudo apt install python3-tk`.

[pygame_examples/glcube.py](pygame_examples/glcube.py) also needs PyOpenGL, which `requirements.txt` installs.

## Framework

This repository contains examples and assets, not the underlying framework. For source code, installation, and framework documentation, see **[Pygame Zero Plus](https://github.com/mjdargen/pgzero)**.
