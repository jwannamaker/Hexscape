import pyglet

from hex import HexOrientation, Hex, HexGrid
from resources import palette


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
    def __init__(self, img: pyglet.image.Texture, x: int, y: int, batch: pyglet.graphics.Batch):
        super().__init__(img, x, y, batch=batch)
        self.health = 12
        self.attack = 6
        self.defense = 4
        
        self.next_position = self.x, self.y
        self.velocity_x = 0
        self.velocity_y = 0
    
    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
    def set_next_position(self, screen_position):
        self.next_position = screen_position