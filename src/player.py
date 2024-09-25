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
    
class Player:
    def __init__(self, grid: HexGrid, batch: pyglet.graphics.Batch):
        self.health = 12
        self.attack = 6
        self.defense = 4
        
        self.position = grid.get_player_position()
        
        
        
    def move(self, direction):
        pass
    
    