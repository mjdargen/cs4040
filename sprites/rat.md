# rat.aseprite
**Image Size:** 128x16

**Frame Size:** 16x16

**Number of Animations:** 4

**Animations:**
- idle_left - row 0 - 2 frames
- idle_right - row 1 - 2 frames
- walk_left - row 2 - 2 frames
- walk_right - row 3 - 2 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "rat.png"
frame_width = 16
frame_height = 16
rat_idle_left = Sprite(filename, frame_width, frame_height, 0, 2, 5)
rat_idle_right = Sprite(filename, frame_width, frame_height, 1, 2, 5)
rat_walk_left = Sprite(filename, frame_width, frame_height, 2, 2, 5)
rat_walk_right = Sprite(filename, frame_width, frame_height, 3, 2, 5)

# Define SpriteActor
rat = SpriteActor(rat_idle_left)
```
