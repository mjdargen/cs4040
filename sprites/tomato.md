# tomato.aseprite
**Image Size:** 352x128

**Frame Size:** 32x32

**Number of Animations:** 4

**Animations:**
- Idle - row 0 - 5 frames
- Jump - row 1 - 8 frames
- Hurt - row 2 - 5 frames
- DeathNoBlood - row 3 - 11 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
tomato_idle = Sprite("tomato", frame_width=32, frame_height=32, row=0, frames=5, fps=5)
tomato_jump = Sprite("tomato", frame_width=32, frame_height=32, row=1, frames=8, fps=5)
tomato_hurt = Sprite("tomato", frame_width=32, frame_height=32, row=2, frames=5, fps=5)
tomato_death_no_blood = Sprite("tomato", frame_width=32, frame_height=32, row=3, frames=11, fps=5)

# Define the Actor
tomato = Actor(tomato_idle)
```
