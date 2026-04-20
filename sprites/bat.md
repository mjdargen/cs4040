# bat.aseprite
**Image Size:** 384x32

**Frame Size:** 32x32

**Number of Animations:** 3

**Animations:**
- Idle - row 0 - 4 frames
- Move - row 1 - 4 frames
- Death - row 2 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "bat.png"
frame_width = 32
frame_height = 32
bat_idle = Sprite(filename, frame_width, frame_height, 0, 4, 5)
bat_move = Sprite(filename, frame_width, frame_height, 1, 4, 5)
bat_death = Sprite(filename, frame_width, frame_height, 2, 4, 5)

# Define SpriteActor
bat = SpriteActor(bat_idle)
```
