# cat.aseprite
**Image Size:** 320x20

**Frame Size:** 32x20

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 4 frames
- walk - row 1 - 6 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "cat.png"
frame_width = 32
frame_height = 20
cat_idle = Sprite(filename, frame_width, frame_height, 0, 4, 5)
cat_walk = Sprite(filename, frame_width, frame_height, 1, 6, 5)

# Define SpriteActor
cat = SpriteActor(cat_idle)
```
