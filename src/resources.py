import string
import json

import numpy as np
from PIL import ImageColor
import pyglet.image
import pyglet
from pyglet.font.user import UserDefinedMappingFont
from pyglet.text.formats.structured import ImageElement


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
values = [pyglet.resource.image(f'{char}.png').get_image_data() for char in keys]
font_mapping = {k: v for k, v in zip(keys, values)}
pyglet.font.add_user_font(UserDefinedMappingFont('pixelator', default_char='A', size=30, 
                                                 mappings=font_mapping))


def center_anchor(img: pyglet.image.TextureRegion):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

hex_wall_image = pyglet.resource.image('hexagon_tile_walls.png')
wall_textures = pyglet.image.ImageGrid(hex_wall_image, rows=1, columns=6, 
                                       item_width=64, item_height=64)
for texture in wall_textures:
    center_anchor(texture)
wall_names = ['UP', 'UP_RIGHT', 'DOWN_RIGHT', 'DOWN', 'DOWN_LEFT', 'UP_LEFT']
tile_walls = {wall_names[i]: wall_textures[i] for i in range(len(wall_names))}

ball_image = pyglet.resource.image('simple_ball_32x32.png')
center_anchor(ball_image)

bop_laser_sound = pyglet.resource.media('bop_laser.wav', False)
click_sound = pyglet.resource.media('click.wav', False)
intro = pyglet.resource.media('intro.mp3', False)
full_track = pyglet.resource.media('Piano_bipFullTrack.wav', True)

# Calculate color fade in/out values
fade_time = 1200 

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
    

arrow_image = pyglet.resource.image('arrow_icons_16x16.png')
arrow_textures = pyglet.image.ImageGrid(arrow_image, rows=1, columns=6,
                                        item_height=16, item_width=16)
keys = ['up_left', 'down_left', 'down', 'down_right', 'up_right', 'up']
arrow_icons = {keys[i]: ImageElement(arrow_textures[i], 32, 28) for i in range(len(keys))}


hex_icon = pyglet.resource.image('dusk-hexagon-64x64.png')
center_anchor(hex_icon)


empty_hud_waypoint = pyglet.resource.image('empty_waypoint_hud_icon_32x32.png')
        