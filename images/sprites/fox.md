# fox.aseprite
**Image Size:** 1344x16

**Frame Size:** 24x16

**Number of Animations:** 7

**Animations:**
- idle - row 0 - 5 frames

- long_idle - row 1 - 14 frames

- walk - row 2 - 8 frames

- jump - row 3 - 11 frames

- hurt - row 4 - 5 frames

- sleep - row 5 - 6 frames

- die - row 6 - 7 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "fox.png"
frame_width = 24
frame_height = 16
fox_idle = Sprite(filename, frame_width, frame_height, 0, 5, 5)
fox_long_idle = Sprite(filename, frame_width, frame_height, 1, 14, 5)
fox_walk = Sprite(filename, frame_width, frame_height, 2, 8, 5)
fox_jump = Sprite(filename, frame_width, frame_height, 3, 11, 5)
fox_hurt = Sprite(filename, frame_width, frame_height, 4, 5, 5)
fox_sleep = Sprite(filename, frame_width, frame_height, 5, 6, 5)
fox_die = Sprite(filename, frame_width, frame_height, 6, 7, 5)

# Define SpriteActor
fox = SpriteActor(fox_idle)
```
