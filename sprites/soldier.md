# soldier.aseprite
**Image Size:** 192x48

**Frame Size:** 24x24

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 6 frames
- walk - row 1 - 8 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
soldier_idle = Sprite("soldier", frame_width=24, frame_height=24, row=0, frames=6, fps=5)
soldier_walk = Sprite("soldier", frame_width=24, frame_height=24, row=1, frames=8, fps=5)

# Define the Actor
soldier = Actor(soldier_idle)
```
