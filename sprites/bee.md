# bee.aseprite
**Image Size:** 256x16

**Frame Size:** 16x16

**Number of Animations:** 4

**Animations:**
- right - row 0 - 4 frames
- left - row 1 - 4 frames
- up - row 2 - 4 frames
- down - row 3 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "bee.png"
frame_width = 16
frame_height = 16
bee_right = Sprite(filename, frame_width, frame_height, 0, 4, 5)
bee_left = Sprite(filename, frame_width, frame_height, 1, 4, 5)
bee_up = Sprite(filename, frame_width, frame_height, 2, 4, 5)
bee_down = Sprite(filename, frame_width, frame_height, 3, 4, 5)

# Define SpriteActor
bee = SpriteActor(bee_right)
```
