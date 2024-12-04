# santa.aseprite
**Image Size:** 640x32

**Frame Size:** 32x32

**Number of Animations:** 3

**Animations:**
- idle - row 0 - 6 frames

- run - row 1 - 6 frames

- jump - row 2 - 8 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "santa.png"
frame_width = 32
frame_height = 32
santa_idle = Sprite(filename, frame_width, frame_height, 0, 6, 5)
santa_run = Sprite(filename, frame_width, frame_height, 1, 6, 5)
santa_jump = Sprite(filename, frame_width, frame_height, 2, 8, 5)

# Define SpriteActor
santa = SpriteActor(santa_idle)
```
