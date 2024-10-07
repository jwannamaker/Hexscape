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
        self.next_position = pyglet.math.Vec2(self.x, self.y)
        self.velocity_x = 0
        self.velocity_y = 0
    
    def move(self, dt):
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        if self.current_position.distance(self.next_position) > 0.1:
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
        else:
            pyglet.clock.unschedule(self.move)
        
    def set_next_position(self, screen_position):
        self.next_position = pyglet.math.Vec2(*screen_position)
        
        velocity = self.next_position - self.current_position
        velocity.normalize()
        self.velocity_x = velocity[0]
        self.velocity_y = velocity[1]
        
    