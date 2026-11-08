# CS4040 — Game Design & Simulation

Example games, starter code and art for **CS4040 Game Design & Simulation**. You'll write 2D games in Python with **[Pygame Zero Plus](https://github.com/mjdargen/pgzero)**, a version of [Pygame Zero](https://github.com/lordmauve/pgzero) with extra features for making games.

## Slides and cheat sheets

**Course home page: [dargen.io/cs4040](https://dargen.io/cs4040/)**

| Module                                      | Slides                                                          | Cheat sheet                                                                                                                        |
| ------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Unit 3 · Module 1: Pygame Zero Basics       | [slides](https://dargen.io/cs4040/course/u3m1/u3m1-slides.html) | [web](https://dargen.io/cs4040/course/u3m1/u3m1-cheatsheet.html) · [PDF](https://dargen.io/cs4040/course/u3m1/u3m1-cheatsheet.pdf) |
| Unit 3 · Module 2: Event-Driven Programming | [slides](https://dargen.io/cs4040/course/u3m2/u3m2-slides.html) | [web](https://dargen.io/cs4040/course/u3m2/u3m2-cheatsheet.html) · [PDF](https://dargen.io/cs4040/course/u3m2/u3m2-cheatsheet.pdf) |
| Unit 3 · Module 3: Collisions & Game State  | [slides](https://dargen.io/cs4040/course/u3m3/u3m3-slides.html) | [web](https://dargen.io/cs4040/course/u3m3/u3m3-cheatsheet.html) · [PDF](https://dargen.io/cs4040/course/u3m3/u3m3-cheatsheet.pdf) |
| Unit 4 · Module 1: Lists & Loops            | [slides](https://dargen.io/cs4040/course/u4m1/u4m1-slides.html) | [web](https://dargen.io/cs4040/course/u4m1/u4m1-cheatsheet.html) · [PDF](https://dargen.io/cs4040/course/u4m1/u4m1-cheatsheet.pdf) |
| Unit 4 · Module 2: Sounds & Music           | [slides](https://dargen.io/cs4040/course/u4m2/u4m2-slides.html) | [web](https://dargen.io/cs4040/course/u4m2/u4m2-cheatsheet.html) · [PDF](https://dargen.io/cs4040/course/u4m2/u4m2-cheatsheet.pdf) |
| Unit 5 · Module 1: Advanced Pygame Zero     | [slides](https://dargen.io/cs4040/course/u5m1/u5m1-slides.html) | [web](https://dargen.io/cs4040/course/u5m1/u5m1-cheatsheet.html) · [PDF](https://dargen.io/cs4040/course/u5m1/u5m1-cheatsheet.pdf) |

## Getting started on your own computer

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

2. Get this repository: clone it, or use **Code → Download ZIP** at the top of this page and unzip it.

   ```bash
   git clone https://github.com/mjdargen/cs4040.git
   cd cs4040
   ```

3. Open the folder in your editor (such as VS Code) and run an example with the Run button, or with `python e00starter.py` from this folder.

Keep your games in this folder, next to `images/`, `sounds/` and the other asset folders. Pygame Zero Plus looks for images, sounds and music in folders beside the program you run.

Every program starts with `import pgzrun` and `from pgzero.builtins import *`, and ends with `pgzrun.go()`. [e00starter.py](e00starter.py) is a blank game to start from.

### Getting the latest examples and art

[utils/update.py](utils/update.py) sets up any folder for this class, with no git needed. Copy it into the folder you work in and run it there (use `python3` on macOS and Linux):

| Command                       | What it does                                   |
| ----------------------------- | ---------------------------------------------- |
| `python update.py pygame`     | installs or updates Pygame Zero Plus           |
| `python update.py all`        | copies in all the examples and the art folders |
| `python update.py examples 5` | copies in examples `e00` through `e05` only    |
| `python update.py assets`     | copies in just the art folders                 |
| `python update.py`            | lists everything else it can do                |

It downloads the newest files from this repository each time, so run it again whenever new examples are added. It replaces the example files with fresh copies, so make your changes in your own file (copy the example and rename it), not in the example itself.

## Example games

The examples are numbered in the order we use them in class: [e00starter.py](e00starter.py) is a blank game, and each one after it adds something new (drawing, moving, the keyboard and mouse, collisions, lists, sound, animated sprites and more). Open one, run it, then change it and see what happens.

## Art, sounds and music

| Folder                        | What's in it                                              |
| ----------------------------- | --------------------------------------------------------- |
| [images/](images/README.md)   | Characters, objects and backgrounds you can use as Actors |
| [sprites/](sprites/README.md) | Animated sprite sheets, with notes on each animation      |
| [sounds/](sounds/README.md)   | Sound effects                                             |
| [music/](music/README.md)     | Background music                                          |
| [maps/](maps/README.md)       | Tiled maps and tile sets                                  |
| [fonts/](fonts/README.md)     | Pixel and monospaced fonts                                |

Each folder's README lists where its files came from. Not all of them share one license, so check before using them in something you publish outside class.

## Making your own sprites

**[Sprite Studio](https://dargen.io/sprite-studio/)** turns your own art into sprite sheets in your browser: sheets, strips, GIFs, Aseprite and Piskel files, and tile sets. It previews the animations and writes the `Sprite(...)` code for you.

The [utils/](utils/) folder also has Python scripts for preparing art and sound:

| Script                      | What it does                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------ |
| `map_and_sprite_checker.py` | Checks that every map, tileset and sprite in `maps/` and `sprites/` loads correctly  |
| `sprite_documenter.py`      | Gives every sprite a `.png`, `.aseprite` and `.md` notes, and warns if a pair disagrees |
| `piskel_unpacker.py`        | Exports frames and a GIF from Piskel files                                           |
| `resolve_tilemaps.py`       | Moves Tiled maps and their tile sets into `maps/` and fixes the paths in them        |
| `convert_audio.py`          | Converts WAV and MP3 files to OGG                                                    |
| `lowercase_filenames.py`    | Renames files to lowercase names that Pygame Zero Plus can load                      |

To install everything these scripts need, run `python -m pip install -r requirements.txt` from this folder. `convert_audio.py` also needs [ffmpeg](https://ffmpeg.org/), and `sprite_documenter.py` needs [Aseprite](https://www.aseprite.org/). Most scripts work on the whole `sprites/` or `maps/` folder at once; for changing one sprite or tile set by hand, use Sprite Studio.

## Pygame Zero Plus

This repository has examples and art, not Pygame Zero Plus itself. For its documentation, see **[pgzero-plus.readthedocs.io](https://pgzero-plus.readthedocs.io/en/latest/)**; for its source code, see **[mjdargen/pgzero](https://github.com/mjdargen/pgzero)**.

---

_Teachers: how the slides, cheat sheets and Codio assignments are made is in [course/README.md](course/README.md)._
