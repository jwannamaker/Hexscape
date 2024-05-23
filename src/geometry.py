from dataclasses import dataclass
from collections import namedtuple

import numpy as np
import pyglet

def x_rotation(point, angle):
    theta = np.deg2rad(angle)
    rot_x = np.array([[1, 0, 0],
                    [0, np.cos(theta), -np.sin(theta)],
                    [0, np.sin(theta), np.cos(theta)]])
    return np.matmul(rot_x, point)

def y_rotation(point, angle):
    theta = np.deg2rad(angle)
    rot_y = np.array([[np.cos(theta), 0, -np.sin(theta)],
                    [0, 1, 0],
                    [np.sin(theta), 0, np.cos(theta)]])
    return np.matmul(rot_y, point)

def z_rotation(point, angle):
    theta = np.deg2rad(angle)
    rot_z = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1]])
    return np.matmul(rot_z, point)

def hexagon(center_x, center_y, radius, batch):
    """ Reusing code from PolyBounce """
    step = 60 # degrees
    start = (180 - step) / 2  # Orients polygon to have a flat ass
    stop = start + 360 + step
    angles = np.arange(np.deg2rad(start), np.deg2rad(stop), np.deg2rad(step))
    vertices = []
    for i, angle in enumerate(angles):
        x = radius * np.cos(angle) + center_x
        y = radius * np.sin(angle) + center_y
        vertices.append([x, y])
        
    hexagon = pyglet.shapes.Polygon(*vertices, batch=batch)
    border = pyglet.shapes.MultiLine(*vertices, thickness=5, color=(200, 200, 200), batch=batch)
    return border


@dataclass
class Hex:
    """ Flat-topped hexagon. """
    Neighbors = {
        'UP_RIGHT': (),
        'UP': (),
        'UP_LEFT': (),
        'DOWN_LEFT': (),
        'DOWN': (),
        'DOWN_RIGHT': ()
    }
    
    def __init__(self, radius):
        

class HexGrid:
    
        
    