from dataclasses import dataclass, field
from collections import namedtuple
import operator
import random

import pyglet
import numpy as np
from numpy.linalg import inv

def x_rotation(point, angle):
    theta = np.deg2rad(angle)
    rot_x = np.array([[1, 0, 0],
                    [0, np.cos(theta), -np.sin(theta)],
                    [0, np.sin(theta), np.cos(theta)]])
    return rot_x @ point

def y_rotation(point, angle):
    theta = np.deg2rad(angle)
    rot_y = np.array([[np.cos(theta), 0, -np.sin(theta)],
                    [0, 1, 0],
                    [np.sin(theta), 0, np.cos(theta)]])
    return rot_y @ point

def z_rotation(point, angle):
    theta = np.deg2rad(angle)
    rot_z = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1]])
    return rot_z @ point

@dataclass
class Hex:
    q: int
    r: int
    s: int
    
    def __post_init__(self):
        assert(self.q + self.r + self.s == 0); 'Invalid: q + r + s != 0'
    
    def __add__(self, other: 'Hex'):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)
    
    def __sub__(self, other: 'Hex'):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)
    
    def __eq__(self, other: 'Hex'):
        return self.q == other.q and self.r == other.r and self.s == other.s
    
    def __hash__(self):
        return hash((self.q, self.r, self.s))
    
    def length(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
    
    def distance_to(self, other: 'Hex'):
        return self.length(self - other)
    
    def vector(self):
        return np.row_stack([self.q, self.r])

class HexOrientation:
    # radius = 64
    # width = 2 * radius
    # height = np.sqrt(3) * radius
    
    i = np.array([3 / 2,  np.sqrt(3) / 2])
    j = np.array([0,      np.sqrt(3)])
    hex_to_pixel = np.column_stack([i, j])
    pixel_to_hex = np.linalg.inv(hex_to_pixel)
    
    corner_angles = np.arange(0, 360, 60)

    @staticmethod
    def center(hex: Hex, radius: int, origin: np.ndarray):
        """ Return the center of the hexagon in pixel coordinates. """
        return ((radius * HexOrientation.hex_to_pixel) @ hex.vector()) + origin

    @staticmethod
    def corners(radius: int, center_x: int, center_y: int):
        corners = []
        for angle in HexOrientation.corner_angles:
            x = radius * np.cos(np.deg2rad(angle)) + center_x
            y = radius * np.sin(np.deg2rad(angle)) + center_y
            corners.append((x, y))
        return corners

    @staticmethod
    def convert_to_hex(radius: int, screen_pos: np.ndarray, origin: np.ndarray):
        """ Convert the screen coordinate to a hexagon coordinate. """
        return HexOrientation.round(((screen_pos - origin) / radius) @ HexOrientation.pixel_to_hex)
    
    ADJACENT_DIRECTION = {
        'UP_RIGHT':   Hex(+1, -1,  0), 
        'UP':         Hex( 0, -1, +1), 
        'UP_LEFT':    Hex(-1,  0, +1),
        'DOWN_RIGHT': Hex(-1, +1,  0), 
        'DOWN':       Hex( 0, +1, -1), 
        'DOWN_LEFT':  Hex(+1,  0, -1)
    }
    
    DIAGONAL_DIRECTION = {
        'RIGHT':           Hex(+2, -1, -1),
        'UP_UP_RIGHT':     Hex(+1, -2, +1),
        'UP_UP_LEFT':      Hex(-1, -1, +2),
        'LEFT':            Hex(-2, +1, +1),
        'DOWN_DOWN_LEFT':  Hex(-1, +2, -1),
        'DOWN_DOWN_RIGHT': Hex(+1, +1, -2)
    }
    
    @staticmethod
    def neighbor(hex: Hex, direction: str):
        """ Return the hex coordinate for the neighbor of hex in direction """
        if direction in HexOrientation.ADJACENT_DIRECTION:
            return hex + HexOrientation.ADJACENT_DIRECTION(direction)
        if direction in HexOrientation.DIAGONAL_DIRECTION:
            return hex + HexOrientation.DIAGONAL_DIRECTION(direction)
        return hex # No neighbor was found, so return the original coordinate
    
    @staticmethod
    def round(frac_q: float, frac_r: float, frac_s: float):
        q = round(q)
        r = round(r)
        s = round(s)
        
        q_diff = abs(q - frac_q)
        r_diff = abs(r - frac_r)
        s_diff = abs(s - frac_s)
        
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
        return Hex(q, r, s)

class HexGrid:
    def __init__(self, radius: int, grid_size: int, origin_x: int, origin_y: int, batch: pyglet.graphics.Batch):
        self._radius = radius
        self._grid_size = grid_size
        self._origin = np.row_stack([origin_x, origin_y])
        self._batch = batch
        
        self._tiles = {}
        for q in range(-self._grid_size, self._grid_size + 1, 1):
            start_r = max(-self._grid_size, -q - self._grid_size)
            stop_r = min(self._grid_size, -q + self._grid_size)
            for r in range(start_r, stop_r + 1, 1):
                s = -q - r
                new_tile = Hex(q, r, s)
                self._tiles[new_tile] = self.tile(new_tile)
    
    def tile(self, hex: Hex):
        """ Eventually return a sprite of the tile. """
        center_x, center_y = HexOrientation.center(hex, 64, self._origin)
        background = pyglet.shapes.Polygon(*HexOrientation.corners(self._radius, center_x, center_y),
                                           color=(255, 100, 67, 255),
                                           batch=self._batch)
        foreground = pyglet.shapes.Polygon(*HexOrientation.corners(self._radius - 10, center_x, center_y),
                                           color=(0, 0, 0, 255),
                                           batch=self._batch)
        return [background, foreground]
        
    def nearby(self, hex: Hex, search_distance: int):
        """ Returns a list of hex coordinates within search_distance to the given 
        hex coordinate.
        Note: The coordinates WILL need to be validated by the map.
        """
        results = []
        for q in range(-search_distance, search_distance + 1, 1):
            # Find only the revelvant values for r to iterate over, considering
            # q + r + s == 0
            start_r = max(-search_distance, -q - search_distance)
            stop_r = min(search_distance, -q + search_distance)
            for r in range(start_r, stop_r + 1, 1):
                s = -q - r
                results.append(hex + Hex(q, r, s))
        return results

    def __contains__(self, key: Hex):
        return key in self._tiles
    
    def highlight(self, screen_x, screen_y):
        # screen_pos = np.row_stack([screen_x, screen_y])
        for tile in self._tiles.values():
            if (screen_x, screen_y) in tile[0]:
                tile[0].color = (255, 255, 255, 255)
                tile[1].color = (random.randint(100, 200), 
                                 random.randint(50, 255),
                                 random.randint(0, 100), 
                                 255)

# if __name__ == '__main__':
    # test_grid = HexGrid()
    