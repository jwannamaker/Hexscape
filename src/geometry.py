"""
Horizontal distance between two adjacent flat top regular hexagons
    h = 3/4 * WIDTH = 3/2 * RADIUS

Vertical distance between two adjacent flat top regular hexagons
    v = HEIGHT = sqrt(3) * RADIUS
"""

from dataclasses import dataclass, field
from collections import namedtuple
import operator

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
    
    def length(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
    
    def distance_to(self, other: 'Hex'):
        return self.length(self - other)
    
    def vector(self):
        return np.row_stack([self.q, self.r])

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

class HexOrientation:
    def __init__(self, origin_x: int, origin_y: int, radius: int = 64, flat_top: bool = True):
        """ (origin_x, origin_y): screen coordinate for center of Hex(0, 0, 0). """
        self._radius = radius
        self._width = 2 * self._radius
        self._height = np.sqrt(3) * self._radius

        self._origin = np.row_stack([origin_x, origin_y])
        self._i = np.array([3 / 2,  np.sqrt(3) / 2])
        self._j = np.array([0,      np.sqrt(3)])
        self._hex_to_pixel = np.column_stack([self._i, self._j])

        if flat_top:
            step = 60 # degrees
            start = (180 - step) / 2  # flat top orientation
            stop = start + 360 + step
        self._corner_angles = np.arange(start, stop, step)

    def center(self, hex: Hex):
        """ Return the center of the hex in pixel coordinates. """
        
        result = self._radius * self._pixel_transformation_matrix @ hex.vector()
        return result + self._origin

    def corners(self, hex):
        corners = []
        center_x, center_y = self.center(hex)
        
        for angle in self._corner_angles:
            x = self._radius * np.cos(np.deg2rad(angle)) + center_x
            y = self._radius * np.sin(np.deg2rad(angle)) + center_y
            corners.append((x, y))
        return corners

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
    
    def neighbor(self, hex: Hex, direction: str):
        """ Return the hex coordinate for the neighbor of hex in direction """
        if direction in HexOrientation.ADJACENT_DIRECTION:
            return hex + HexOrientation.ADJACENT_DIRECTION(direction)
        if direction in HexOrientation.DIAGONAL_DIRECTION:
            return hex + HexOrientation.DIAGONAL_DIRECTION(direction)
        return hex # No neighbor was found, so return the original coordinate
    
class HexLayout:
    def __init__(self, orientation: HexOrientation, batch: pyglet.graphics.Batch):
        self.HexTiles = {}
        
    def nearby(self, hex: Hex, search_distance: int):
        """ Returns a list of hex coordinates within search_distance to the given 
        hex coordinate.
        Note: The coordinates WILL need to be validated by the map.
        """
        results = []
        for q in range(-search_distance, search_distance, 1):
            # Find only the revelvant values for r to iterate over, considering
            # q + r + s == 0
            start_r = max(-search_distance, -q - search_distance)
            stop_r = min(search_distance, -q + search_distance)
            for r in range(start_r, stop_r, 1):
                s = -q - r
                results.append(hex + Hex(q, r, s))
        return results
            

    

if __name__ == '__main__':
    orientation = HexOrientation(0, 0, 10)
    bestagon = Hex(0, 0, 0)
    print(orientation.corners(bestagon))
    