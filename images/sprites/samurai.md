# samurai.aseprite
**Image Size:** 960x32

**Frame Size:** 24x32

**Number of Animations:** 6

**Animations:**
- idle - row 0 - 8 frames
- run - row 1 - 8 frames
- jump - row 2 - 4 frames
- fall - row 3 - 4 frames
- hurt - row 4 - 2 frames
- die - row 5 - 14 frames

**Code Example:**
```python
# Sprite(filename, frame_width, frame_height, row_number, frame_count, fps)
# Note: FPS set to 5 in examples below, adjust as needed)
filename = "samurai.png"
frame_width = 24
frame_height = 32
samurai_idle = Sprite(filename, frame_width, frame_height, 0, 8, 5)
samurai_run = Sprite(filename, frame_width, frame_height, 1, 8, 5)
samurai_jump = Sprite(filename, frame_width, frame_height, 2, 4, 5)
samurai_fall = Sprite(filename, frame_width, frame_height, 3, 4, 5)
samurai_hurt = Sprite(filename, frame_width, frame_height, 4, 2, 5)
samurai_die = Sprite(filename, frame_width, frame_height, 5, 14, 5)

# Define SpriteActor
samurai = SpriteActor(samurai_idle)
```
