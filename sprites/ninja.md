# ninja.aseprite
**Image Size:** 2560x32

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
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "ninja.png"
frame_width = 32
frame_height = 32
ninja_idle_down = Sprite(filename, frame_width, frame_height, 0, 4, 5)
ninja_idle_up = Sprite(filename, frame_width, frame_height, 1, 4, 5)
ninja_idle_left = Sprite(filename, frame_width, frame_height, 2, 4, 5)
ninja_idle_right = Sprite(filename, frame_width, frame_height, 3, 4, 5)
ninja_walk_down = Sprite(filename, frame_width, frame_height, 4, 4, 5)
ninja_walk_up = Sprite(filename, frame_width, frame_height, 5, 4, 5)
ninja_walk_left = Sprite(filename, frame_width, frame_height, 6, 4, 5)
ninja_walk_right = Sprite(filename, frame_width, frame_height, 7, 4, 5)
ninja_attack_down = Sprite(filename, frame_width, frame_height, 8, 4, 5)
ninja_attack_up = Sprite(filename, frame_width, frame_height, 9, 4, 5)
ninja_attack_left = Sprite(filename, frame_width, frame_height, 10, 4, 5)
ninja_attack_right = Sprite(filename, frame_width, frame_height, 11, 4, 5)
ninja_jump_down = Sprite(filename, frame_width, frame_height, 12, 3, 5)
ninja_jump_up = Sprite(filename, frame_width, frame_height, 13, 3, 5)
ninja_jump_left = Sprite(filename, frame_width, frame_height, 14, 3, 5)
ninja_jump_right = Sprite(filename, frame_width, frame_height, 15, 3, 5)
ninja_roll_down = Sprite(filename, frame_width, frame_height, 16, 3, 5)
ninja_roll_up = Sprite(filename, frame_width, frame_height, 17, 3, 5)
ninja_roll_left = Sprite(filename, frame_width, frame_height, 18, 3, 5)
ninja_roll_right = Sprite(filename, frame_width, frame_height, 19, 3, 5)
ninja_hit_down = Sprite(filename, frame_width, frame_height, 20, 2, 5)
ninja_hit_up = Sprite(filename, frame_width, frame_height, 21, 2, 5)
ninja_hit_left = Sprite(filename, frame_width, frame_height, 22, 2, 5)
ninja_hit_right = Sprite(filename, frame_width, frame_height, 23, 2, 5)

# Define SpriteActor
ninja = SpriteActor(ninja_idle_down)
```
