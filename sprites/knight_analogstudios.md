# knight_analogstudios.aseprite
**Image Size:** 512x160

**Frame Size:** 32x32

**Number of Animations:** 5

**Animations:**
- idle - row 0 - 4 frames
- run - row 1 - 16 frames
- roll - row 2 - 8 frames
- hit - row 3 - 4 frames
- death - row 4 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
knight_analogstudios_idle = Sprite("knight_analogstudios", frame_width=32, frame_height=32, row=0, frames=4, fps=5)
knight_analogstudios_run = Sprite("knight_analogstudios", frame_width=32, frame_height=32, row=1, frames=16, fps=5)
knight_analogstudios_roll = Sprite("knight_analogstudios", frame_width=32, frame_height=32, row=2, frames=8, fps=5)
knight_analogstudios_hit = Sprite("knight_analogstudios", frame_width=32, frame_height=32, row=3, frames=4, fps=5)
knight_analogstudios_death = Sprite("knight_analogstudios", frame_width=32, frame_height=32, row=4, frames=4, fps=5)

# Define the Actor
knight_analogstudios = Actor(knight_analogstudios_idle)
```
