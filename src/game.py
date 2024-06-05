import datetime
import time

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from circle import Circle
from font import Font
from button import Button
from hex import HexGrid
from timer import Timer
from resources import palette, hex_image

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)
main_window.set_icon(hex_image)
background_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()

circle_manager = Circle()
font_manager = Font(64, 64, main_window.width, main_window.height, main_batch)
button_manager = Button(main_window)
timer = Timer(main_window.width, main_window.height, background_batch)

font_manager.write('Level 1', 0, main_window.height-64)
grid = HexGrid(32, 6, main_window.width//2, main_window.height//2, background_batch)

clock = pyglet.clock.get_default()
clock.schedule_interval(timer.update, 1/60.0)

@main_window.event
def on_key_press(symbol, modifiers):
    if key.P:
        screenshot_name = f'screenshot {datetime.datetime.now().strftime('%a %m-%d-%Y %H:%M')}.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
    if key.ENTER:
        pass
    
    if key.W:
        grid.move_player('UP')
    if key.W & key.A:
        grid.move_player('UP_LEFT')
    if key.A:
        grid.move_player('LEFT')
    if key.A & key.S:
        grid.move_player('DOWN_LEFT')
    if key.S:
        grid.move_player('DOWN')
    if key.S & key.D:
        grid.move_player('DOWN_RIGHT')
    if key.D:
        grid.move_player('RIGHT')
    if key.W & key.D:
        grid.move_player('UP_RIGHT')


@main_window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.RIGHT:
        # circle_manager.draw_circle(x, y, main_batch)
        grid.highlight_again(x, y)
        
        for box in font_manager.border_boxes:
            if (x, y) in box:
                box.color = palette['red'][0]
                

@main_window.event
def on_mouse_motion(x, y, dx, dy):
    grid.highlight(x, y)

@main_window.event
def on_draw():
    main_window.clear()
    background_batch.draw()
    main_batch.draw()
    
    
if __name__ == '__main__':
    pyglet.app.run()