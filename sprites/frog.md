# frog.aseprite
**Image Size:** 192x48

**Frame Size:** 24x24

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 7 frames
- hop - row 1 - 8 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
frog_idle = Sprite("frog", frame_width=24, frame_height=24, row=0, frames=7, fps=5)
frog_hop = Sprite("frog", frame_width=24, frame_height=24, row=1, frames=8, fps=5)

# Define the Actor
frog = Actor(frog_idle)
```
