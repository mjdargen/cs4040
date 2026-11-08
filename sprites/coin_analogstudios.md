# coin_analogstudios.aseprite
**Image Size:** 192x16

**Frame Size:** 16x16

**Number of Animations:** 1

**Animations:**
- spin - row 0 - 12 frames

**Code Example:**
```python
# Note: fps is set to 5 below; adjust as needed
coin_analogstudios_spin = Sprite("coin_analogstudios", frame_width=16, frame_height=16, row=0, frames=12, fps=5)

# Define the Actor
coin_analogstudios = Actor(coin_analogstudios_spin)
```
