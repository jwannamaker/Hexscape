import datetime
import time

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from circle import Circle
from font import Font
from button import Button
from geometry import HexGrid


gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

pyglet.resource.path = ['../resources', '../resources/font', '../resources/button']
pyglet.resource.reindex()

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)
background_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()

circle_manager = Circle()
font_manager = Font(64, 128, main_window.width, main_window.height, main_batch)
button_manager = Button(main_window)

font_manager.write('WARPOOL', 0, main_window.height-128)
grid = HexGrid(64, 3, main_window.width//2, main_window.height//2, background_batch)

@main_window.event
def on_key_press(symbol, modifiers):
    if key.MOD_CTRL & modifiers:
        screenshot_name = f'screenshot {datetime.datetime.now().strftime('%a %m-%d-%Y %H:%M')}.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
        
@main_window.event
def on_mouse_press(x, y, button, modifiers):
    """ Possible values:
        pyglet.window.mouse.LEFT
        pyglet.window.mouse.MIDDLE
        pyglet.window.mouse.RIGHT
    """
    if button == mouse.LEFT:
        # circle_manager.draw_circle(x, y, main_batch)
        grid.highlight(x, y)


@main_window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y < 0:
        circle_manager.dec_radius()
    if scroll_y > 0:
        circle_manager.inc_radius()

@main_window.event
def on_draw():
    main_window.clear()
    background_batch.draw()
    main_batch.draw()
    

if __name__ == '__main__':
    pyglet.app.run()