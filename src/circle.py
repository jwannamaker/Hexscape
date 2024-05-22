import random

import pyglet

class Circle:
    colors = {
        "deep-purple": (39, 24, 57),
        "mid-purple": (60, 45, 92),
        "indigo-blue": (67, 63, 119),
        "mid-blue": (79, 91, 132),
        "light-blue": (109, 128, 155),
        "seafoam-green": (159, 195, 173)
    }
    
    def __init__(self):
        self.circles = []
        self.radius = 10

    def dec_radius(self):
        if self.radius > 10:
            self.radius += -1

    def inc_radius(self):
        if self.radius < 100:
            self.radius += 1

    def draw_circle(self, x, y, batch):
        self.circles.append(pyglet.shapes.Circle(x=x, y=y, radius=self.radius, 
                                            color=random.choice(list(Circle.colors.values())), 
                                            batch=batch))