# soldier.aseprite
**Image Size:** 336x24

**Frame Size:** 24x24

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 6 frames
- walk - row 1 - 8 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "soldier.png"
frame_width = 24
frame_height = 24
soldier_idle = Sprite(filename, frame_width, frame_height, 0, 6, 5)
soldier_walk = Sprite(filename, frame_width, frame_height, 1, 8, 5)

# Define SpriteActor
soldier = SpriteActor(soldier_idle)
```
