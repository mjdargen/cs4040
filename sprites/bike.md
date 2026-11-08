# bike.aseprite
**Image Size:** 1024x128

**Frame Size:** 64x64

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 4 frames
- pedal - row 1 - 16 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
bike_idle = Sprite("bike", frame_width=64, frame_height=64, row=0, frames=4, fps=5)
bike_pedal = Sprite("bike", frame_width=64, frame_height=64, row=1, frames=16, fps=5)

# Define the Actor
bike = Actor(bike_idle)
```
