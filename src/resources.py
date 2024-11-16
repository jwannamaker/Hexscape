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

hex_wall_image = pyglet.resource.image('hexagon_tile_walls.png')
wall_textures = pyglet.image.ImageGrid(hex_wall_image, rows=1, columns=6, 
                                       item_width=64, item_height=64)
for texture in wall_textures:
    center_anchor(texture)
wall_names = ['UP', 'UP_RIGHT', 'DOWN_RIGHT', 'DOWN', 'DOWN_LEFT', 'UP_LEFT']
tile_walls = {wall_names[i]: wall_textures[i] for i in range(len(wall_names))}

ball_image = pyglet.resource.image('simple-ball-32x32.png')
center_anchor(ball_image)

bop_laser_sound = pyglet.resource.media('bop_laser.wav', False)
click_sound = pyglet.resource.media('click.wav', False)
intro = pyglet.resource.media('intro.mp3', False)
full_track = pyglet.resource.media('Piano_bipFullTrack.wav', True)

# Calculate color fade in/out values
fade_time = 12000

control_pt_1 = pyglet.math.Vec2(0, 255)
control_pt_2 = pyglet.math.Vec2(400, 70)
control_pt_3 = pyglet.math.Vec2(700, 255)
control_pt_4 = pyglet.math.Vec2(fade_time, 0)

fade_out = {}
for t in range(0, fade_time):
    alpha = t / fade_time
    midpoint_a = control_pt_1.lerp(control_pt_2, alpha)
    midpoint_b = control_pt_2.lerp(control_pt_3, alpha)
    midpoint_c = control_pt_3.lerp(control_pt_4, alpha)
    
    midpoint_d = midpoint_a.lerp(midpoint_b, alpha)
    midpoint_e = midpoint_b.lerp(midpoint_c, alpha)
    
    point = midpoint_d.lerp(midpoint_e, alpha)
    fade_out[t] = round(point.y)

