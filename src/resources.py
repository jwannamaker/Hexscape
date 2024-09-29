import string
import json

import pyglet
from PIL import ImageColor

pyglet.resource.path = ['../resources', 
                        '../resources/audio', 
                        '../resources/button', 
                        '../resources/font', 
                        '../resources/images']
pyglet.resource.reindex()

""" 
A dict for the palette with 
    k: string name of colors
    v: RGB int tuple
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

hex_image = pyglet.resource.image('dusk-hexagon-64x64.png')
hex_image.anchor_x = hex_image.width // 2
hex_image.anchor_y = hex_image.height // 2