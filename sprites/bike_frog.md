# bike_frog.aseprite
**Image Size:** 960x64

**Frame Size:** 64x64

**Number of Animations:** 1

**Animations:**
- move - row 0 - 15 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
bike_frog_move = Sprite("bike_frog", frame_width=64, frame_height=64, row=0, frames=15, fps=5)

# Define the Actor
bike_frog = Actor(bike_frog_move)
```
