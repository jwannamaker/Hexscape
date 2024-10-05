import datetime
import time
from collections import namedtuple

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from circle import Circle
from font import Font
from button import Button
from hex import HexGrid
from player import Player
from timer import Timer
from resources import palette, hex_image, ball_image

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
highlight_color = 'purple'
clock = pyglet.clock.get_default()
player = Player(img=ball_image, 
                x=main_window.width//2, 
                y=main_window.height//2,
                batch=main_batch)
board = HexGrid(radius=32, 
                grid_size=6, 
                origin_x=main_window.width//2, 
                origin_y=main_window.height//2, 
                batch=background_batch,
                player=player)

@main_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.P:
        screenshot_name = f'screenshot {datetime.datetime.now().strftime('%a %m-%d-%Y %H:%M')}.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
    
    """ Note: Axes are flipped and not in the intuitive orientation. """
    if symbol == key.Q:
        board.move_player('DOWN_RIGHT')
        clock.schedule(player.move)
    if symbol == key.W:
        board.move_player('DOWN')
        clock.schedule(player.move)
    if symbol == key.E:
        board.move_player('DOWN_LEFT')
        clock.schedule(player.move)
    if symbol == key.A:
        board.move_player('UP_LEFT')
        clock.schedule(player.move)
    if symbol == key.S:
        board.move_player('UP')
        clock.schedule(player.move)
    if symbol == key.D:
        board.move_player('UP_RIGHT')
        clock.schedule(player.move)
    
@main_window.event
def on_draw():
    main_window.clear()
    background_batch.draw()
    main_batch.draw()
    
if __name__ == '__main__':
    pyglet.app.run()