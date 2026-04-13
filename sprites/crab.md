# crab.aseprite
**Image Size:** 512x16

**Frame Size:** 32x16

**Number of Animations:** 4

**Animations:**
- idle - row 0 - 4 frames
- walk - row 1 - 4 frames
- die - row 2 - 4 frames
- attack - row 3 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "crab.png"
frame_width = 32
frame_height = 16
crab_idle = Sprite(filename, frame_width, frame_height, 0, 4, 5)
crab_walk = Sprite(filename, frame_width, frame_height, 1, 4, 5)
crab_die = Sprite(filename, frame_width, frame_height, 2, 4, 5)
crab_attack = Sprite(filename, frame_width, frame_height, 3, 4, 5)

# Define SpriteActor
crab = SpriteActor(crab_idle)
```
