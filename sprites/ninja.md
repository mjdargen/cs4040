# ninja.aseprite
**Image Size:** 128x768

**Frame Size:** 32x32

**Number of Animations:** 24

**Animations:**
- idle_down - row 0 - 4 frames
- idle_up - row 1 - 4 frames
- idle_left - row 2 - 4 frames
- idle_right - row 3 - 4 frames
- walk_down - row 4 - 4 frames
- walk_up - row 5 - 4 frames
- walk_left - row 6 - 4 frames
- walk_right - row 7 - 4 frames
- attack_down - row 8 - 4 frames
- attack_up - row 9 - 4 frames
- attack_left - row 10 - 4 frames
- attack_right - row 11 - 4 frames
- jump_down - row 12 - 3 frames
- jump_up - row 13 - 3 frames
- jump_left - row 14 - 3 frames
- jump_right - row 15 - 3 frames
- roll_down - row 16 - 3 frames
- roll_up - row 17 - 3 frames
- roll_left - row 18 - 3 frames
- roll_right - row 19 - 3 frames
- hit_down - row 20 - 2 frames
- hit_up - row 21 - 2 frames
- hit_left - row 22 - 2 frames
- hit_right - row 23 - 2 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
ninja_idle_down = Sprite("ninja", frame_width=32, frame_height=32, row=0, frames=4, fps=5)
ninja_idle_up = Sprite("ninja", frame_width=32, frame_height=32, row=1, frames=4, fps=5)
ninja_idle_left = Sprite("ninja", frame_width=32, frame_height=32, row=2, frames=4, fps=5)
ninja_idle_right = Sprite("ninja", frame_width=32, frame_height=32, row=3, frames=4, fps=5)
ninja_walk_down = Sprite("ninja", frame_width=32, frame_height=32, row=4, frames=4, fps=5)
ninja_walk_up = Sprite("ninja", frame_width=32, frame_height=32, row=5, frames=4, fps=5)
ninja_walk_left = Sprite("ninja", frame_width=32, frame_height=32, row=6, frames=4, fps=5)
ninja_walk_right = Sprite("ninja", frame_width=32, frame_height=32, row=7, frames=4, fps=5)
ninja_attack_down = Sprite("ninja", frame_width=32, frame_height=32, row=8, frames=4, fps=5)
ninja_attack_up = Sprite("ninja", frame_width=32, frame_height=32, row=9, frames=4, fps=5)
ninja_attack_left = Sprite("ninja", frame_width=32, frame_height=32, row=10, frames=4, fps=5)
ninja_attack_right = Sprite("ninja", frame_width=32, frame_height=32, row=11, frames=4, fps=5)
ninja_jump_down = Sprite("ninja", frame_width=32, frame_height=32, row=12, frames=3, fps=5)
ninja_jump_up = Sprite("ninja", frame_width=32, frame_height=32, row=13, frames=3, fps=5)
ninja_jump_left = Sprite("ninja", frame_width=32, frame_height=32, row=14, frames=3, fps=5)
ninja_jump_right = Sprite("ninja", frame_width=32, frame_height=32, row=15, frames=3, fps=5)
ninja_roll_down = Sprite("ninja", frame_width=32, frame_height=32, row=16, frames=3, fps=5)
ninja_roll_up = Sprite("ninja", frame_width=32, frame_height=32, row=17, frames=3, fps=5)
ninja_roll_left = Sprite("ninja", frame_width=32, frame_height=32, row=18, frames=3, fps=5)
ninja_roll_right = Sprite("ninja", frame_width=32, frame_height=32, row=19, frames=3, fps=5)
ninja_hit_down = Sprite("ninja", frame_width=32, frame_height=32, row=20, frames=2, fps=5)
ninja_hit_up = Sprite("ninja", frame_width=32, frame_height=32, row=21, frames=2, fps=5)
ninja_hit_left = Sprite("ninja", frame_width=32, frame_height=32, row=22, frames=2, fps=5)
ninja_hit_right = Sprite("ninja", frame_width=32, frame_height=32, row=23, frames=2, fps=5)

# Define the Actor
ninja = Actor(ninja_idle_down)
```
