# bat.aseprite
**Image Size:** 384x32

**Frame Size:** 32x32

**Number of Animations:** 3

**Animations:**
- Idle - row 0 - 4 frames
- Move - row 1 - 4 frames
- Death - row 2 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
bat_idle = Sprite("bat", frame_width=32, frame_height=32, row=0, frames=4, fps=5)
bat_move = Sprite("bat", frame_width=32, frame_height=32, row=1, frames=4, fps=5)
bat_death = Sprite("bat", frame_width=32, frame_height=32, row=2, frames=4, fps=5)

# Define the Actor
bat = Actor(bat_idle)
```
