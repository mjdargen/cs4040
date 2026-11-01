# piggy.aseprite
**Image Size:** 100x40

**Frame Size:** 20x20

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 5 frames
- walk - row 1 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
piggy_idle = Sprite("piggy", frame_width=20, frame_height=20, row=0, frames=5, fps=5)
piggy_walk = Sprite("piggy", frame_width=20, frame_height=20, row=1, frames=4, fps=5)

# Define the Actor
piggy = Actor(piggy_idle)
```
