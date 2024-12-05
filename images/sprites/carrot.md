# carrot.aseprite
**Image Size:** 1472x32

**Frame Size:** 32x32

**Number of Animations:** 5

**Animations:**
- Idle - row 0 - 5 frames
- Jump - row 1 - 8 frames
- Spin - row 2 - 20 frames
- Hurt - row 3 - 5 frames
- Death - row 4 - 8 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "carrot.png"
frame_width = 32
frame_height = 32
carrot_idle = Sprite(filename, frame_width, frame_height, 0, 5, 5)
carrot_jump = Sprite(filename, frame_width, frame_height, 1, 8, 5)
carrot_spin = Sprite(filename, frame_width, frame_height, 2, 20, 5)
carrot_hurt = Sprite(filename, frame_width, frame_height, 3, 5, 5)
carrot_death = Sprite(filename, frame_width, frame_height, 4, 8, 5)

# Define SpriteActor
carrot = SpriteActor(carrot_idle)
```
