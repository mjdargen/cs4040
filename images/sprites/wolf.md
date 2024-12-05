# wolf.aseprite
**Image Size:** 576x24

**Frame Size:** 24x24

**Number of Animations:** 8

**Animations:**
- idle_front - row 0 - 2 frames
- idle_left - row 1 - 2 frames
- idle_right - row 2 - 2 frames
- idle_back - row 3 - 2 frames
- walk_front - row 4 - 4 frames
- walk_left - row 5 - 4 frames
- walk_right - row 6 - 4 frames
- walk_back - row 7 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "wolf.png"
frame_width = 24
frame_height = 24
wolf_idle_front = Sprite(filename, frame_width, frame_height, 0, 2, 5)
wolf_idle_left = Sprite(filename, frame_width, frame_height, 1, 2, 5)
wolf_idle_right = Sprite(filename, frame_width, frame_height, 2, 2, 5)
wolf_idle_back = Sprite(filename, frame_width, frame_height, 3, 2, 5)
wolf_walk_front = Sprite(filename, frame_width, frame_height, 4, 4, 5)
wolf_walk_left = Sprite(filename, frame_width, frame_height, 5, 4, 5)
wolf_walk_right = Sprite(filename, frame_width, frame_height, 6, 4, 5)
wolf_walk_back = Sprite(filename, frame_width, frame_height, 7, 4, 5)

# Define SpriteActor
wolf = SpriteActor(wolf_idle_front)
```
