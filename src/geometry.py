from dataclasses import dataclass, field
from collections import namedtuple
import operator

import numpy as np
import pyglet

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

# def hexagon(center_x, center_y, radius, batch):
#     """ Reusing code from PolyBounce """
#     step = 60 # degrees
#     start = (180 - step) / 2  # flat top orientation
#     stop = start + 360 + step
#     angles = np.arange(np.deg2rad(start), np.deg2rad(stop), np.deg2rad(step))
#     vertices = []
#     for i, angle in enumerate(angles):
#         x = radius * np.cos(angle) + center_x
#         y = radius * np.sin(angle) + center_y
#         vertices.append([x, y])
        
#     hexagon = pyglet.shapes.Polygon(*vertices, batch=batch)
#     border = pyglet.shapes.MultiLine(*vertices, thickness=5, color=(200, 200, 200), batch=batch)
#     return border

class HexOrientation:
    def __init__(self, radius=64, flat_top=True):
        self.RADIUS = radius
        self.WIDTH = 2 * self.RADIUS
        self.HEIGHT = np.sqrt(3) * self.RADIUS

        self.HORIZONTAL_DISTANCE = 3 / 4 * self.WIDTH
        self.VERTICAL_DISTANCE = self.HEIGHT

        if flat_top:
            step = 60 # degrees
            start = (180 - step) / 2  # flat top orientation
            stop = start + 360 + step
        self.CORNER_ANGLES = np.arange(start, stop, step)

    ADJACENT_DIRECTION = {
        'UP_RIGHT':   (+1, -1,  0), 
        'UP':         ( 0, -1, +1), 
        'UP_LEFT':    (-1,  0, +1),
        'DOWN_RIGHT': (-1, +1,  0), 
        'DOWN':       ( 0, +1, -1), 
        'DOWN_LEFT':  (+1,  0, -1)
    }
    
    def adjacent_neighbor(self, hex, direction):
        return 
    
    DIAGONAL_DIRECTION = {
        'RIGHT':      (+2, -1, -1),
        'UP_RIGHT':   (+1, -2, +1),
        'UP_LEFT':    (-1, -1, +2),
        'LEFT':       (-2, +1, +1),
        'DOWN_LEFT':  (-1, +2, -1),
        'DOWN_RIGHT': (+1, +1, -2)
    }
    
    def diagonal_neighbor(self, hex, diagonal):
        return
        
"""
Horizontal distance between two adjacent flat top regular hexagons
    h = 3/4 * WIDTH = 3/2 * RADIUS

Vertical distance between two adjacent flat top regular hexagons
    v = HEIGHT = sqrt(3) * radius
"""

@dataclass
class Hex:
    q: int
    r: int
    s: int
    
    def __post_init__(self):
        assert(self.q + self.r + self.s == 0); 'Invalid: q + r + s must be zero'
    
    def __add__(self, other: 'Hex'):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)
    
    def __sub__(self, other: 'Hex'):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)
    
    def length(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
    
    def distance_to(self, other: 'Hex'):
        return self.length(self - other)
    
    def up_right(self):
        return operator.add(self, Hex(+1, -1, 0))
    
    def up(self):
        return operator.add(self, Hex(0, -1, +1))
    
    def up_left(self):
        return operator.add(self, Hex(-1, 0, +1))
    
    def down_left(self):
        return operator.add(self, Hex(-1, +1, 0))
    
    def down(self):
        return operator.add(self, Hex(0, +1, -1))
    
    def down_right(self):
        return operator.add(self, Hex(+1, 0, -1))
    
    
@dataclass
class HexTile: 
    hex_coord: Hex
    center: tuple[int, int] = field(kw_only=True)
    
    

if __name__ == '__main__':
    bestagon = Hex(0, 0)
    print(bestagon)
    print(bestagon.corners(150, 150))
    print(bestagon.up())
    print(bestagon.up().corners())