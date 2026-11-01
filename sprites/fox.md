# fox.aseprite
**Image Size:** 336x112

**Frame Size:** 24x16

**Number of Animations:** 7

**Animations:**
- idle - row 0 - 5 frames
- long_idle - row 1 - 14 frames
- walk - row 2 - 8 frames
- jump - row 3 - 11 frames
- hurt - row 4 - 5 frames
- sleep - row 5 - 6 frames
- die - row 6 - 7 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
fox_idle = Sprite("fox", frame_width=24, frame_height=16, row=0, frames=5, fps=5)
fox_long_idle = Sprite("fox", frame_width=24, frame_height=16, row=1, frames=14, fps=5)
fox_walk = Sprite("fox", frame_width=24, frame_height=16, row=2, frames=8, fps=5)
fox_jump = Sprite("fox", frame_width=24, frame_height=16, row=3, frames=11, fps=5)
fox_hurt = Sprite("fox", frame_width=24, frame_height=16, row=4, frames=5, fps=5)
fox_sleep = Sprite("fox", frame_width=24, frame_height=16, row=5, frames=6, fps=5)
fox_die = Sprite("fox", frame_width=24, frame_height=16, row=6, frames=7, fps=5)

# Define the Actor
fox = Actor(fox_idle)
```
