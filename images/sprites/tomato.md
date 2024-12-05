# tomato.aseprite
**Image Size:** 3968x64

**Frame Size:** 64x64

**Number of Animations:** 6

**Animations:**
- Idle - row 0 - 5 frames
- Jump - row 1 - 8 frames
- Attack - row 2 - 22 frames
- Hurt - row 3 - 5 frames
- Death - row 4 - 11 frames
- DeathNoBlood - row 5 - 11 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "tomato.png"
frame_width = 64
frame_height = 64
tomato_idle = Sprite(filename, frame_width, frame_height, 0, 5, 5)
tomato_jump = Sprite(filename, frame_width, frame_height, 1, 8, 5)
tomato_attack = Sprite(filename, frame_width, frame_height, 2, 22, 5)
tomato_hurt = Sprite(filename, frame_width, frame_height, 3, 5, 5)
tomato_death = Sprite(filename, frame_width, frame_height, 4, 11, 5)
tomato_death_no_blood = Sprite(filename, frame_width, frame_height, 5, 11, 5)

# Define SpriteActor
tomato = SpriteActor(tomato_idle)
```
