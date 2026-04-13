# bike_frog.aseprite
**Image Size:** 1024x64

**Frame Size:** 64x64

**Number of Animations:** 1

**Animations:**
- move - row 0 - 15 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "bike_frog.png"
frame_width = 64
frame_height = 64
bike_frog_move = Sprite(filename, frame_width, frame_height, 0, 15, 5)

# Define SpriteActor
bike_frog = SpriteActor(bike_frog_move)
```
