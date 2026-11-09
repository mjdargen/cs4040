"""Find out why a Pygame Zero Plus game is slow or laggy.

It runs your game and measures how long update() and draw() take each frame,
then lists the functions that took the most time. To run at 60 frames a
second, update() and draw() together need to take less than 16.7 ms.

Play the game as usual, then close the window to see the report:

    python profile_game.py ../my_game.py             (Windows)
    python3 profile_game.py ../my_game.py            (macOS and Linux)

Or run it without a window for a few seconds, holding the arrow keys (right,
down, left, up) so the player moves around. This gives the same results every
time, which is handy for checking whether a change made the game faster:

    python profile_game.py ../my_game.py --auto
    python profile_game.py ../my_game.py --auto --seconds 10

Needs Pygame Zero Plus (pip install pgzero-plus).
"""
import argparse
import cProfile
import os
import pstats
import runpy
import sys
import time
from pathlib import Path

SLOWEST = 12  # how many of the slowest functions to list
FRAME_BUDGET = 1000 / 60  # milliseconds per frame for 60 frames a second


def parse_args():
    parser = argparse.ArgumentParser(description="Measure how long each frame of a Pygame Zero Plus game takes.")
    parser.add_argument("game", help="the game's .py file")
    parser.add_argument("--auto", action="store_true", help="run without a window, holding the arrow keys")
    parser.add_argument("--seconds", type=float, default=4, help="how long --auto runs for (default 4)")
    return parser.parse_args()


def main():
    args = parse_args()
    game_file = Path(args.game).resolve()
    if not game_file.is_file():
        sys.exit(f"Can't find {args.game}")

    if args.auto:
        os.environ["SDL_VIDEODRIVER"] = "dummy"  # no window
        os.environ["SDL_AUDIODRIVER"] = "dummy"  # no sound
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

    import pygame
    import pgzero.game as pgz_game

    times = {"update": [], "draw": []}
    total_frames = round(args.seconds * 60)
    arrows = [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]
    frame = 0

    if args.auto:
        # Run as fast as possible for a set number of frames, instead of in
        # real time until the window is closed.
        def frames(fps):
            for _ in range(total_frames):
                yield 1 / 60

        pgz_game.frames = frames

    # Only update() and draw() are profiled, not loading the game or opening
    # the window, which happen once and would crowd the list.
    profiler = cProfile.Profile()
    handle_events = pgz_game.PGZeroGame.handle_events
    get_draw_func = pgz_game.PGZeroGame.get_draw_func

    def timed_handle_events(self, dt, update):
        # update() runs inside handle_events(), along with the clock and keys
        nonlocal frame
        if args.auto:
            for key in arrows:
                self.keyboard._release(key)
            self.keyboard._press(arrows[frame * len(arrows) // total_frames])
        frame += 1
        start = time.perf_counter()
        profiler.enable()
        try:
            return handle_events(self, dt, update)
        finally:
            profiler.disable()
            times["update"].append(time.perf_counter() - start)

    def timed_get_draw_func(self):
        draw = get_draw_func(self)

        def timed_draw():
            start = time.perf_counter()
            profiler.enable()
            try:
                draw()
            finally:
                profiler.disable()
                times["draw"].append(time.perf_counter() - start)

        return timed_draw

    pgz_game.PGZeroGame.handle_events = timed_handle_events
    pgz_game.PGZeroGame.get_draw_func = timed_get_draw_func

    print(f"Running {game_file.name}" + (" without a window..." if args.auto else ". Close the window to see the report."))
    sys.argv = [str(game_file)]
    try:
        runpy.run_path(str(game_file), run_name="__main__")
    except SystemExit:
        pass  # closing the window, or the end of --auto

    report(times, profiler, game_file)


def report(times, profiler, game_file):
    if not times["update"]:
        print("\nThe game stopped before its first frame, so there is nothing to report.")
        return

    print(f"\n{game_file.name}: {len(times['update'])} frames")
    total = 0
    for name in ("update", "draw"):
        ms = sorted(1000 * t for t in times[name]) or [0]
        average = sum(ms) / len(ms)
        total += average
        print(f"  {name + '()':9} average {average:5.1f} ms   slowest {ms[-1]:6.1f} ms")
    verdict = "fast enough" if total < FRAME_BUDGET else "TOO SLOW: it will lag"
    print(f"  together  average {total:5.1f} ms   (60 frames a second needs under {FRAME_BUDGET:.1f} ms: {verdict})")
    print("  One slow frame at the start is normal: images, sounds and fonts load then.")
    print("  Measuring slows the game down a little, so without it the game runs a bit faster.")

    print(f"\nThe {SLOWEST} functions that took the most time in update() and draw()")
    print("(not counting the functions they called):")
    stats = pstats.Stats(profiler)
    rows = sorted(stats.stats.items(), key=lambda item: item[1][2], reverse=True)[:SLOWEST]
    print(f"  {'total ms':>9} {'calls':>9}  function")
    for (filename, line, name), (_, calls, own_time, _, _) in rows:
        where = Path(filename).name if filename not in ("~", "") else "built-in"
        if Path(filename).resolve() == game_file:
            where = f"YOUR GAME, line {line}"
        print(f"  {1000 * own_time:9.1f} {calls:9}  {name}  ({where})")
    print("\nFunctions in YOUR GAME near the top are the first place to look. If")
    print("functions from Pygame Zero Plus are at the top, try fewer Actors or tiles,")
    print("or ask your teacher.")


if __name__ == "__main__":
    main()
