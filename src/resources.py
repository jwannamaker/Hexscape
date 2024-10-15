import string
import json

import pyglet
import numpy as np
from PIL import ImageColor

pyglet.resource.path = ['../resources', 
                        '../resources/audio', 
                        '../resources/button', 
                        '../resources/font', 
                        '../resources/images']
pyglet.resource.reindex()

""" 
A dict for the palette with 
    k: string name of color
    v: list of RGB int tuples
"""
palette: dict[str, int] = json.load(pyglet.resource.file('palette.json'))
for key in palette:
    converted_values = []
    for value in palette[key]:
        converted_values.append(ImageColor.getrgb(value))
    palette[key] = converted_values

keys = [*string.ascii_uppercase, *string.digits]
values = [pyglet.resource.image(f'{char}.png') for char in keys]
font = {k: v for k, v in zip(keys, values)}

def center_anchor(img: pyglet.image.TextureRegion):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

hex_image = pyglet.resource.image('dusk-hexagon-64x64.png')
center_anchor(hex_image)

ball_image = pyglet.resource.image('simple-ball-32x32.png')
center_anchor(ball_image)

bop_laser_sound = pyglet.resource.media('bop_laser.wav', False)
click_sound = pyglet.resource.media('click.wav', False)
intro = pyglet.resource.media('intro.mp3', False)
full_track = pyglet.resource.media('Piano_bipFullTrack.wav', True)

# Find color fade in/out values
control_pt_1 = pyglet.math.Vec2(0, 255)
control_pt_2 = pyglet.math.Vec2(40, 255)
control_pt_3 = pyglet.math.Vec2(16, 130)
control_pt_4 = pyglet.math.Vec2(60, 128)

def fade_out():
    t = 0.0
    while t < 10.0:
        midpoint_a = control_pt_1.lerp(control_pt_2, t)
        midpoint_b = control_pt_2.lerp(control_pt_3, t)
        midpoint_c = control_pt_3.lerp(control_pt_4, t)
        
        midpoint_d = midpoint_a.lerp(midpoint_b, t)
        midpoint_e = midpoint_b.lerp(midpoint_c, t)
        
        point = midpoint_d.lerp(midpoint_e, t)
        yield point.y
        
        t += 1.0
    

