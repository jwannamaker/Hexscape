import numpy as np
import pyglet
import matplotlib.pyplot as plt

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

def square(center_x, center_y, radius, batch):
    """ Reusing code from PolyBounce """
    step = 60 # degrees
    start = (180 - step) / 2  # Orients polygon to have a flat ass
    stop = start + 360 + step
    angles = np.arange(np.deg2rad(start), np.deg2rad(stop), np.deg2rad(step))
    vertices = np.full((7), 0.0)
    for i, point in enumerate(vertices):
        point[0] = np.cos(angles[i]), np.sin(angles[i])
        
    hexagon = pyglet.shapes.Polygon(vertices, batch=batch)
    return hexagon

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
    return hexagon

class Tile:
    def __init__(self, batch):
        self.batch = batch
        self.tiles = []
    
    def draw(self, vertices):
        self.tiles.append(pyglet.shapes.Polygon(vertices, batch=self.batch))
        