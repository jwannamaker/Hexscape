import datetime
import time

import pyglet
from pyglet import gl
from pyglet.window import key, mouse


# Allows images to load with their alpha values blended? 
# I definitely need to learn how OpenGL works. (Eventually)
# gl.glEnable(gl.GL_BLEND)
# gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)

circles = []
main_batch = pyglet.graphics.Batch()
print(f'main_batch is {main_batch}')

def draw_circle(x, y):
    circles.append(pyglet.shapes.Circle(x=x, y=y, radius=10, color=(255, 255, 255, 255), batch=main_batch))

@main_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.P:
        screenshot_name = f'screenshot {datetime.datetime.now().strftime('%m-%d-%Y')}.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)

@main_window.event
def on_mouse_press(x, y, button, modifiers):
    """ Possible values:
        pyglet.window.mouse.LEFT
        pyglet.window.mouse.MIDDLE
        pyglet.window.mouse.RIGHT
    """
    if button == mouse.LEFT:
        print(f'Mouse click @ {x}, {y}')
        draw_circle(x, y)

@main_window.event
def on_draw():
    main_window.clear()
    main_batch.draw()
    for circle in circles:
        circle.draw()

if __name__ == '__main__':
    pyglet.app.run()