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
        'UP_RIGHT':   Hex(+1, -1,  0), # E
        'UP':         Hex( 0, -1, +1), # W
        'UP_LEFT':    Hex(-1,  0, +1), # Q
        'DOWN_RIGHT': Hex(-1, +1,  0), # D
        'DOWN':       Hex( 0, +1, -1), # S
        'DOWN_LEFT':  Hex(+1,  0, -1)  # A
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

# class Player:
#     def __init__(self, initial_position: Hex):
#         self._hex = initial_position
#         self._color = palette['red'][0]
        
#     def place(self, new_position):
#         self._hex = new_position
        
#     def move(self, direction: str):
#         self._hex = HexOrientation.neighbor(self._hex, direction)

