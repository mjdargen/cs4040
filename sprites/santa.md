# santa.aseprite
**Image Size:** 256x96

**Frame Size:** 32x32

**Number of Animations:** 3

**Animations:**
- idle - row 0 - 6 frames
- run - row 1 - 6 frames
- jump - row 2 - 8 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
santa_idle = Sprite("santa", frame_width=32, frame_height=32, row=0, frames=6, fps=5)
santa_run = Sprite("santa", frame_width=32, frame_height=32, row=1, frames=6, fps=5)
santa_jump = Sprite("santa", frame_width=32, frame_height=32, row=2, frames=8, fps=5)

# Define the Actor
santa = Actor(santa_idle)
```
