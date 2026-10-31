# crab.aseprite
**Image Size:** 512x16

**Frame Size:** 32x16

**Number of Animations:** 4

**Animations:**
- idle - row 0 - 4 frames
- walk - row 1 - 4 frames
- die - row 2 - 4 frames
- attack - row 3 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
crab_idle = Sprite("crab", frame_width=32, frame_height=16, row=0, frames=4, fps=5)
crab_walk = Sprite("crab", frame_width=32, frame_height=16, row=1, frames=4, fps=5)
crab_die = Sprite("crab", frame_width=32, frame_height=16, row=2, frames=4, fps=5)
crab_attack = Sprite("crab", frame_width=32, frame_height=16, row=3, frames=4, fps=5)

# Define the Actor
crab = Actor(crab_idle)
```
