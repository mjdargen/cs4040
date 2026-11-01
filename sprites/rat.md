# rat.aseprite
**Image Size:** 32x64

**Frame Size:** 16x16

**Number of Animations:** 4

**Animations:**
- idle_left - row 0 - 2 frames
- idle_right - row 1 - 2 frames
- walk_left - row 2 - 2 frames
- walk_right - row 3 - 2 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
rat_idle_left = Sprite("rat", frame_width=16, frame_height=16, row=0, frames=2, fps=5)
rat_idle_right = Sprite("rat", frame_width=16, frame_height=16, row=1, frames=2, fps=5)
rat_walk_left = Sprite("rat", frame_width=16, frame_height=16, row=2, frames=2, fps=5)
rat_walk_right = Sprite("rat", frame_width=16, frame_height=16, row=3, frames=2, fps=5)

# Define the Actor
rat = Actor(rat_idle_left)
```
