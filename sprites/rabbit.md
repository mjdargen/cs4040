# rabbit.aseprite
**Image Size:** 384x16

**Frame Size:** 16x16

**Number of Animations:** 8

**Animations:**
- idle_down - row 0 - 2 frames
- idle_up - row 1 - 2 frames
- idle_left - row 2 - 2 frames
- idle_right - row 3 - 2 frames
- walk_down - row 4 - 4 frames
- walk_up - row 5 - 4 frames
- walk_left - row 6 - 4 frames
- walk_right - row 7 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
rabbit_idle_down = Sprite("rabbit", frame_width=16, frame_height=16, row=0, frames=2, fps=5)
rabbit_idle_up = Sprite("rabbit", frame_width=16, frame_height=16, row=1, frames=2, fps=5)
rabbit_idle_left = Sprite("rabbit", frame_width=16, frame_height=16, row=2, frames=2, fps=5)
rabbit_idle_right = Sprite("rabbit", frame_width=16, frame_height=16, row=3, frames=2, fps=5)
rabbit_walk_down = Sprite("rabbit", frame_width=16, frame_height=16, row=4, frames=4, fps=5)
rabbit_walk_up = Sprite("rabbit", frame_width=16, frame_height=16, row=5, frames=4, fps=5)
rabbit_walk_left = Sprite("rabbit", frame_width=16, frame_height=16, row=6, frames=4, fps=5)
rabbit_walk_right = Sprite("rabbit", frame_width=16, frame_height=16, row=7, frames=4, fps=5)

# Define the Actor
rabbit = Actor(rabbit_idle_down)
```
