# cow_pixelboy.aseprite
**Image Size:** 32x16

**Frame Size:** 16x16

**Number of Animations:** 1

**Animations:**
- walk - row 0 - 2 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
cow_pixelboy_walk = Sprite("cow_pixelboy", frame_width=16, frame_height=16, row=0, frames=2, fps=5)

# Define the Actor
cow_pixelboy = Actor(cow_pixelboy_walk)
```
