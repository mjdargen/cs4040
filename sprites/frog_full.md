# frog_full.aseprite
**Image Size:** 324x100

**Frame Size:** 36x20

**Number of Animations:** 5

**Animations:**
- idle - row 0 - 8 frames
- jump - row 1 - 7 frames
- eat - row 2 - 6 frames
- hurt - row 3 - 4 frames
- die - row 4 - 9 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
frog_full_idle = Sprite("frog_full", frame_width=36, frame_height=20, row=0, frames=8, fps=5)
frog_full_jump = Sprite("frog_full", frame_width=36, frame_height=20, row=1, frames=7, fps=5)
frog_full_eat = Sprite("frog_full", frame_width=36, frame_height=20, row=2, frames=6, fps=5)
frog_full_hurt = Sprite("frog_full", frame_width=36, frame_height=20, row=3, frames=4, fps=5)
frog_full_die = Sprite("frog_full", frame_width=36, frame_height=20, row=4, frames=9, fps=5)

# Define the Actor
frog_full = Actor(frog_full_idle)
```
