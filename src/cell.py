from hex import Hex, HexOrientation as hex_util
from resources import palette, tile_walls


import numpy as np
import pyglet


class HexCell:
    def __init__(self, hex_coordinate: Hex, radius: int, screen_origin: np.ndarray,
                 background_color: str, batch: pyglet.graphics.Batch):
        self.hex_coordinate = hex_coordinate

        self.center_x = hex_util.center(self.hex_coordinate, radius, screen_origin)[0]
        self.center_y = hex_util.center(self.hex_coordinate, radius, screen_origin)[1]
        self.background = pyglet.shapes.Polygon(*hex_util.corners(radius, self.center_x, self.center_y),
                                                color=palette[background_color][0],
                                                batch=batch)
        self.background.opacity = 0

        # For maze generation
        self.walls = {neighbor: True for neighbor in hex_util.neighbors(self.hex_coordinate)}
        self.visited = False

    def wall_sprite(self, wall: str, batch: pyglet.graphics.Batch):
        return pyglet.sprite.Sprite(tile_walls[wall], x=self.center_x, y=self.center_y,
                                    batch=batch)

    def coordinate(self):
        return self.hex_coordinate

    def visit(self):
        self.visited = True

    def unvisited(self):
        return not self.visited

    def remove_wall(self, neighbor: 'HexCell'):
        if self.walls[neighbor.coordinate()]:
            self.walls[neighbor.coordinate()] = False

    def neighbors(self):
        """ Returns the list of all neighbors that don't have a wall between them. """
        neighbors = []
        for neighbor, wall in list(self.walls.items()):
            if not wall:
                neighbors.append(neighbor)
        return neighbors

    def fade(self, opacity):
        self.background.opacity = opacity

    def highlight(self):
        self.background.opacity = 255