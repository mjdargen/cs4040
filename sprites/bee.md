# bee.aseprite
**Image Size:** 256x16

**Frame Size:** 16x16

**Number of Animations:** 4

**Animations:**
- right - row 0 - 4 frames
- left - row 1 - 4 frames
- up - row 2 - 4 frames
- down - row 3 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
bee_right = Sprite("bee", frame_width=16, frame_height=16, row=0, frames=4, fps=5)
bee_left = Sprite("bee", frame_width=16, frame_height=16, row=1, frames=4, fps=5)
bee_up = Sprite("bee", frame_width=16, frame_height=16, row=2, frames=4, fps=5)
bee_down = Sprite("bee", frame_width=16, frame_height=16, row=3, frames=4, fps=5)

# Define the Actor
bee = Actor(bee_right)
```
