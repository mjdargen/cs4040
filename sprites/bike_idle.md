# bike_idle.aseprite
**Image Size:** 256x64

**Frame Size:** 64x64

**Number of Animations:** 1

**Animations:**
- idle - row 0 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
bike_idle_idle = Sprite("bike_idle", frame_width=64, frame_height=64, row=0, frames=4, fps=5)

# Define the Actor
bike_idle = Actor(bike_idle_idle)
```
