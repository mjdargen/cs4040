# carrot.aseprite
**Image Size:** 640x160

**Frame Size:** 32x32

**Number of Animations:** 5

**Animations:**
- Idle - row 0 - 5 frames
- Jump - row 1 - 8 frames
- Spin - row 2 - 20 frames
- Hurt - row 3 - 5 frames
- Death - row 4 - 8 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
carrot_idle = Sprite("carrot", frame_width=32, frame_height=32, row=0, frames=5, fps=5)
carrot_jump = Sprite("carrot", frame_width=32, frame_height=32, row=1, frames=8, fps=5)
carrot_spin = Sprite("carrot", frame_width=32, frame_height=32, row=2, frames=20, fps=5)
carrot_hurt = Sprite("carrot", frame_width=32, frame_height=32, row=3, frames=5, fps=5)
carrot_death = Sprite("carrot", frame_width=32, frame_height=32, row=4, frames=8, fps=5)

# Define the Actor
carrot = Actor(carrot_idle)
```
