# bike_idle.aseprite
**Image Size:** 256x64

**Frame Size:** 64x64

**Number of Animations:** 1

**Animations:**
- idle - row 0 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "bike_idle.png"
frame_width = 64
frame_height = 64
bike_idle_idle = Sprite(filename, frame_width, frame_height, 0, 4, 5)

# Define SpriteActor
bike_idle = SpriteActor(bike_idle_idle)
```
