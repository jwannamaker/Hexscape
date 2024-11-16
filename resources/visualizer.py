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
    
tile_width, tile_height = 100, 100
window = pyglet.window.Window(tile_width*len(palette), tile_height*4)
# window.set_fullscreen(True)
general_batch = pyglet.graphics.Batch()
        
rectangles = []
j = 0
for key in list(palette.keys()):
    for i in range(len(palette[key])):
        rectangle = pyglet.shapes.Rectangle(x=j, y=i*tile_height, 
                                            width=tile_width, height=tile_height,
                                            color=palette[key][i], 
                                            batch=general_batch)
        rectangles.append(rectangle)
    j += tile_width

@window.event
def on_draw():
    window.clear()
    general_batch.draw()

@window.event
def on_key_release(symbol, modifiers):
    pyglet.image.get_buffer_manager().get_color_buffer().save('palette.png')
    
if __name__ == '__main__':
    pyglet.app.run()