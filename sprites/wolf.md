# wolf.aseprite
**Image Size:** 576x24

**Frame Size:** 24x24

**Number of Animations:** 8

**Animations:**
- idle_down - row 0 - 2 frames
- idle_left - row 1 - 2 frames
- idle_right - row 2 - 2 frames
- idle_up - row 3 - 2 frames
- walk_down - row 4 - 4 frames
- walk_left - row 5 - 4 frames
- walk_right - row 6 - 4 frames
- walk_up - row 7 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
wolf_idle_down = Sprite("wolf", frame_width=24, frame_height=24, row=0, frames=2, fps=5)
wolf_idle_left = Sprite("wolf", frame_width=24, frame_height=24, row=1, frames=2, fps=5)
wolf_idle_right = Sprite("wolf", frame_width=24, frame_height=24, row=2, frames=2, fps=5)
wolf_idle_up = Sprite("wolf", frame_width=24, frame_height=24, row=3, frames=2, fps=5)
wolf_walk_down = Sprite("wolf", frame_width=24, frame_height=24, row=4, frames=4, fps=5)
wolf_walk_left = Sprite("wolf", frame_width=24, frame_height=24, row=5, frames=4, fps=5)
wolf_walk_right = Sprite("wolf", frame_width=24, frame_height=24, row=6, frames=4, fps=5)
wolf_walk_up = Sprite("wolf", frame_width=24, frame_height=24, row=7, frames=4, fps=5)

# Define the Actor
wolf = Actor(wolf_idle_down)
```
