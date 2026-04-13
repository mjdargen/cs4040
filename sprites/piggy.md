# piggy.aseprite
**Image Size:** 180x20

**Frame Size:** 20x20

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 5 frames
- walk - row 1 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "piggy.png"
frame_width = 20
frame_height = 20
piggy_idle = Sprite(filename, frame_width, frame_height, 0, 5, 5)
piggy_walk = Sprite(filename, frame_width, frame_height, 1, 4, 5)

# Define SpriteActor
piggy = SpriteActor(piggy_idle)
```
