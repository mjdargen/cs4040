# snake_pixelboy.aseprite
**Image Size:** 64x64

**Frame Size:** 16x16

**Number of Animations:** 4

**Animations:**
- walk_down - row 0 - 4 frames
- walk_up - row 1 - 4 frames
- walk_left - row 2 - 4 frames
- walk_right - row 3 - 4 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
snake_pixelboy_walk_down = Sprite("snake_pixelboy", frame_width=16, frame_height=16, row=0, frames=4, fps=5)
snake_pixelboy_walk_up = Sprite("snake_pixelboy", frame_width=16, frame_height=16, row=1, frames=4, fps=5)
snake_pixelboy_walk_left = Sprite("snake_pixelboy", frame_width=16, frame_height=16, row=2, frames=4, fps=5)
snake_pixelboy_walk_right = Sprite("snake_pixelboy", frame_width=16, frame_height=16, row=3, frames=4, fps=5)

# Define the Actor
snake_pixelboy = Actor(snake_pixelboy_walk_down)
```
