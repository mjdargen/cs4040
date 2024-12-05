# frog.aseprite
**Image Size:** 360x24

**Frame Size:** 24x24

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 7 frames
- hop - row 1 - 8 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "frog.png"
frame_width = 24
frame_height = 24
frog_idle = Sprite(filename, frame_width, frame_height, 0, 7, 5)
frog_hop = Sprite(filename, frame_width, frame_height, 1, 8, 5)

# Define SpriteActor
frog = SpriteActor(frog_idle)
```
