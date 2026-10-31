# cat.aseprite
**Image Size:** 320x20

**Frame Size:** 32x20

**Number of Animations:** 2

**Animations:**
- idle - row 0 - 4 frames
- walk - row 1 - 6 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
cat_idle = Sprite("cat", frame_width=32, frame_height=20, row=0, frames=4, fps=5)
cat_walk = Sprite("cat", frame_width=32, frame_height=20, row=1, frames=6, fps=5)

# Define the Actor
cat = Actor(cat_idle)
```
