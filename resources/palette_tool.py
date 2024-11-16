import json
import pyglet
from pyglet import gl
from PIL import ImageColor

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


def convert(hex_color_string):
    return ImageColor.getrgb(hex_color_string)

palette = json.load(pyglet.resource.file('palette.json'))
for key in palette:
    converted_values = []
    for value in palette[key]:
        converted_values.append(ImageColor.getrgb(value))
    palette[key] = converted_values
    print(key, converted_values)
    
tile_width, tile_height = 100, 100
window = pyglet.window.Window(tile_width*len(palette), tile_height*4 + tile_height//2)
general_batch = pyglet.graphics.Batch()

name_label = pyglet.text.Label('color_name', font_size=28, x=0, y=10, batch=general_batch)
rgb_label = pyglet.text.Label('(0, 0, 0)', font_size=14, x=window.width//3, y=34, batch=general_batch)
hex_label = pyglet.text.Label('#ffffffff', font_size=14, x=window.width//3, y=10, batch=general_batch)

rectangles = []
j = 0
for key in list(palette.keys()):
    for i in range(len(palette[key])):
        rectangle = pyglet.shapes.Rectangle(x=j, y=i*tile_height + tile_height//2, 
                                            width=tile_width, height=tile_height,
                                            color=palette[key][i], 
                                            batch=general_batch)
        rectangles.append(rectangle)
    j += tile_width

def has_color(color, color_list):
    for c in color_list:
        if color == c:
            return True
    return False

def get_color_name(color):
    for item in list(palette.items()):
        if color in item[1]:
            return str(item[0])
    return 'not found'

def get_color_num(color):
    for item in list(palette.items()):
        if color in item[1]:
            return item[1].index(color)
    return 0

@window.event
def on_draw():
    window.clear()
    general_batch.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    for rectangle in rectangles:
        if (x, y) in rectangle:
            name_label.text = f'palette[\'{get_color_name(rectangle.color)}\'][{get_color_num(rectangle.color)}]'
            rgb_label.text = str(rectangle.color)
            hex_label.text = '#' + str(hex(rectangle.color[0]))[2:] + \
                                   str(hex(rectangle.color[1]))[2:] + \
                                   str(hex(rectangle.color[2]))[2:] + \
                                   str(hex(rectangle.color[3]))[2:]

@window.event
def on_mouse_release(x, y, button, modifiers):
    pyglet.image.get_buffer_manager().get_color_buffer().save('palette.png')
    
if __name__ == '__main__':
    pyglet.app.run()