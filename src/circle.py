import random

import pyglet


colors = {
    "deep-purple": (39, 24, 57),
    "mid-purple": (60, 45, 92),
    "indigo-blue": (67, 63, 119),
    "mid-blue": (79, 91, 132),
    "light-blue": (109, 128, 155),
    "seafoam-green": (159, 195, 173)
}
circles = []


radius = 10

def dec_radius():
    global radius
    
    if radius > 10:
        radius += -1

def inc_radius():
    global radius
    
    if radius < 100:
        radius += 1
    


def draw_circle(x, y, batch):
    global radius
    
    circles.append(pyglet.shapes.Circle(x=x, y=y, radius=radius, 
                                        color=random.choice(list(colors.values())), 
                                        batch=batch))