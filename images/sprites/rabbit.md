# rabbit.aseprite
**Image Size:** 384x16

**Frame Size:** 16x16

**Number of Animations:** 8

**Animations:**
- idle_front - row 0 - 2 frames

- idle_back - row 1 - 2 frames

- idle_left - row 2 - 2 frames

- idle_right - row 3 - 2 frames

- walk_front - row 4 - 4 frames

- walk_back - row 5 - 4 frames

- walk_left - row 6 - 4 frames

- wake_right - row 7 - 4 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "rabbit.png"
frame_width = 16
frame_height = 16
rabbit_idle_front = Sprite(filename, frame_width, frame_height, 0, 2, 5)
rabbit_idle_back = Sprite(filename, frame_width, frame_height, 1, 2, 5)
rabbit_idle_left = Sprite(filename, frame_width, frame_height, 2, 2, 5)
rabbit_idle_right = Sprite(filename, frame_width, frame_height, 3, 2, 5)
rabbit_walk_front = Sprite(filename, frame_width, frame_height, 4, 4, 5)
rabbit_walk_back = Sprite(filename, frame_width, frame_height, 5, 4, 5)
rabbit_walk_left = Sprite(filename, frame_width, frame_height, 6, 4, 5)
rabbit_wake_right = Sprite(filename, frame_width, frame_height, 7, 4, 5)

# Define SpriteActor
rabbit = SpriteActor(rabbit_idle_front)
```
