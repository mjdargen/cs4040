# tomato_simple.aseprite
**Image Size:** 928x32

**Frame Size:** 32x32

**Number of Animations:** 4

**Animations:**
- Idle - row 0 - 5 frames

- Jump - row 1 - 8 frames

- Hurt - row 2 - 5 frames

- DeathNoBlood - row 3 - 11 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "tomato_simple.png"
frame_width = 32
frame_height = 32
tomato_simple_idle = Sprite(filename, frame_width, frame_height, 0, 5, 5)
tomato_simple_jump = Sprite(filename, frame_width, frame_height, 1, 8, 5)
tomato_simple_hurt = Sprite(filename, frame_width, frame_height, 2, 5, 5)
tomato_simple_death_no_blood = Sprite(filename, frame_width, frame_height, 3, 11, 5)

# Define SpriteActor
tomato_simple = SpriteActor(tomato_simple_idle)
```
