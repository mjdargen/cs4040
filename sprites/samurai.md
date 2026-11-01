# samurai.aseprite
**Image Size:** 336x192

**Frame Size:** 24x32

**Number of Animations:** 6

**Animations:**
- idle - row 0 - 8 frames
- run - row 1 - 8 frames
- jump - row 2 - 4 frames
- fall - row 3 - 4 frames
- hurt - row 4 - 2 frames
- die - row 5 - 14 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
samurai_idle = Sprite("samurai", frame_width=24, frame_height=32, row=0, frames=8, fps=5)
samurai_run = Sprite("samurai", frame_width=24, frame_height=32, row=1, frames=8, fps=5)
samurai_jump = Sprite("samurai", frame_width=24, frame_height=32, row=2, frames=4, fps=5)
samurai_fall = Sprite("samurai", frame_width=24, frame_height=32, row=3, frames=4, fps=5)
samurai_hurt = Sprite("samurai", frame_width=24, frame_height=32, row=4, frames=2, fps=5)
samurai_die = Sprite("samurai", frame_width=24, frame_height=32, row=5, frames=14, fps=5)

# Define the Actor
samurai = Actor(samurai_idle)
```
