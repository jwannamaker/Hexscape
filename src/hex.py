from dataclasses import dataclass
from collections import deque

import numpy as np

"""
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
"""


@dataclass
class Hex:
    """ Baseclass for anything taking place on a hexagonal grid. """
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
        return (self - other).length()
    
    def vector(self):
        return np.row_stack([self.q, self.r])

class HexOrientation:
    i = np.array([3 / 2,  np.sqrt(3) / 2])
    j = np.array([0,      np.sqrt(3)])
    hex_to_pixel = np.column_stack([i, j])
    pixel_to_hex = np.linalg.inv(hex_to_pixel)

    @staticmethod
    def center(hex: Hex, radius: int, origin: np.ndarray):
        """ Return the center of the hexagon in pixel coordinates. """
        center = ((radius * HexOrientation.hex_to_pixel) @ hex.vector()) + origin
        return round(center[0][0]), round(center[1][0])

    @staticmethod
    def corners(radius: int, center_x: int, center_y: int):
        corners = []
        for angle in np.arange(0, 360, 60):
            x = radius * np.cos(np.deg2rad(angle)) + center_x
            y = radius * np.sin(np.deg2rad(angle)) + center_y
            corners.append((x, y))
        return corners

    @staticmethod
    def convert_to_hex(radius: int, screen_pos: np.ndarray, origin: np.ndarray):
        """ Convert the screen coordinate to a hexagon coordinate. """
        return HexOrientation.round(((screen_pos - origin) / radius) @ HexOrientation.pixel_to_hex)
    
    ADJACENT_DIRECTION = {             # Prev    NOW
        'UP_RIGHT':   Hex(+1,  0, -1), # D       E
        'UP':         Hex( 0, +1, -1), # S       W
        'UP_LEFT':    Hex(-1, +1,  0), # A       Q
        'DOWN_RIGHT': Hex(+1, -1,  0), # Q       D
        'DOWN':       Hex( 0, -1, +1), # W       S
        'DOWN_LEFT':  Hex(-1,  0, +1)  # E       A
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
            return hex + HexOrientation.ADJACENT_DIRECTION[direction]
        if direction in HexOrientation.DIAGONAL_DIRECTION:
            return hex + HexOrientation.DIAGONAL_DIRECTION[direction]
        return hex # No neighbor was found, so return the original coordinate
    
    @staticmethod
    def neighbors(hex: Hex):
        return [hex + direction for direction in list(HexOrientation.ADJACENT_DIRECTION.values())]
    
    @staticmethod
    def search_nearby(hex: Hex, search_distance: int):
        """ Returns a list of hex coordinates within search_distance to the given 
        hex coordinate.
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
    
def generate_square_grid(grid_size):
    coordinates: list[Hex] = []
    for q in range(-grid_size, grid_size + 1, 1):
        start_r = max(-grid_size, -q - grid_size)
        stop_r = min(grid_size, -q + grid_size)
        for r in range(start_r, stop_r + 1, 1):
            s = -q - r
            coordinates.append(Hex(q, r, s))
    return coordinates