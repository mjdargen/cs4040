# panda.aseprite
**Image Size:** 1176x16

**Frame Size:** 24x16

**Number of Animations:** 7

**Animations:**
- 1 - row 0 - 6 frames
- 2 - row 1 - 6 frames
- 3 - row 2 - 8 frames
- 4 - row 3 - 8 frames
- 5 - row 4 - 5 frames
- 6 - row 5 - 8 frames
- 7 - row 6 - 8 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
panda_1 = Sprite("panda", frame_width=24, frame_height=16, row=0, frames=6, fps=5)
panda_2 = Sprite("panda", frame_width=24, frame_height=16, row=1, frames=6, fps=5)
panda_3 = Sprite("panda", frame_width=24, frame_height=16, row=2, frames=8, fps=5)
panda_4 = Sprite("panda", frame_width=24, frame_height=16, row=3, frames=8, fps=5)
panda_5 = Sprite("panda", frame_width=24, frame_height=16, row=4, frames=5, fps=5)
panda_6 = Sprite("panda", frame_width=24, frame_height=16, row=5, frames=8, fps=5)
panda_7 = Sprite("panda", frame_width=24, frame_height=16, row=6, frames=8, fps=5)

# Define the Actor
panda = Actor(panda_1)
```
