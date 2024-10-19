from collections import deque

import pyglet
import numpy as np

"""
# STATUS STATS
- health points + any boosters
- attack points + any boosters
- defense points + any boosters

# LEVEL STATS *[could potentially move to a different class]
- current level 
- score

# ACTION STATS
- available moves
- number of moves left
- available attack patterns

## Note

- Player is really just a sprite, and will interact with the board by requesting 
the appropriate info for
    - ACTION STATS
    - Positioning the sprite in the center of a certain grid tile
    - Getting the tile position by using the board's ability to convert screen 
    coordinates into tile positions and vice versa

"""
    
class Player(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.Texture, x: int, y: int, 
                 batch: pyglet.graphics.Batch):
        super().__init__(img, x, y, batch=batch)
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        self.next_position = deque([])
        self._movable = True
    
    def movable(self):
        return self._movable
    
    def move(self, dt):
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        destination = self.current_position if len(self.next_position) == 0 else self.next_position[0]
        distance = self.current_position.distance(destination)
        if distance > 1:
            self._movable = False
            self.x += ((destination[0] - self.x) / distance) * dt * 100
            self.y += ((destination[1] - self.y) / distance) * dt * 100
        else:
            self._movable = True
            if len(self.next_position) > 0:
                self.next_position.popleft()
            pyglet.clock.unschedule(self.move)
        
    def add_next_position(self, screen_position):
        position = pyglet.math.Vec2(*screen_position)
        if position not in self.next_position:
            self.next_position.append(pyglet.math.Vec2(*screen_position))
        
    