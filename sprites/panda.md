# panda.aseprite
**Image Size:** 1176x16

**Frame Size:** 24x16

**Number of Animations:** 7

**Animations:**
- 1 - row 0 - 6 frames
- 2 - row 1 - 6 frames
- 3 - row 2 - 8 frames
- 4 - row 3 - 8 frames
- 5 - row 4 - 5 frames
- 6 - row 5 - 8 frames
- 7 - row 6 - 8 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "panda.png"
frame_width = 24
frame_height = 16
panda_1 = Sprite(filename, frame_width, frame_height, 0, 6, 5)
panda_2 = Sprite(filename, frame_width, frame_height, 1, 6, 5)
panda_3 = Sprite(filename, frame_width, frame_height, 2, 8, 5)
panda_4 = Sprite(filename, frame_width, frame_height, 3, 8, 5)
panda_5 = Sprite(filename, frame_width, frame_height, 4, 5, 5)
panda_6 = Sprite(filename, frame_width, frame_height, 5, 8, 5)
panda_7 = Sprite(filename, frame_width, frame_height, 6, 8, 5)

# Define SpriteActor
panda = SpriteActor(panda_1)
```
