# giant_frog_pixelboy.aseprite
**Image Size:** 280x200

**Frame Size:** 40x40

**Number of Animations:** 5

**Animations:**
- idle - row 0 - 5 frames
- jump - row 1 - 6 frames
- charge - row 2 - 7 frames
- attack - row 3 - 3 frames
- hit - row 4 - 3 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
giant_frog_pixelboy_idle = Sprite("giant_frog_pixelboy", frame_width=40, frame_height=40, row=0, frames=5, fps=5)
giant_frog_pixelboy_jump = Sprite("giant_frog_pixelboy", frame_width=40, frame_height=40, row=1, frames=6, fps=5)
giant_frog_pixelboy_charge = Sprite("giant_frog_pixelboy", frame_width=40, frame_height=40, row=2, frames=7, fps=5)
giant_frog_pixelboy_attack = Sprite("giant_frog_pixelboy", frame_width=40, frame_height=40, row=3, frames=3, fps=5)
giant_frog_pixelboy_hit = Sprite("giant_frog_pixelboy", frame_width=40, frame_height=40, row=4, frames=3, fps=5)

# Define the Actor
giant_frog_pixelboy = Actor(giant_frog_pixelboy_idle)
```
