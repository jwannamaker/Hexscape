import datetime
import time
from collections import namedtuple

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from board import HexBoard, HexCell
from font import Font
from player import Player
from resources import palette, hex_image, ball_image, intro, full_track

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)
main_window.set_icon(hex_image)
background_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()
background_color = pyglet.shapes.Rectangle(0, 0, main_window.width, main_window.height,
                                           color=palette['black'][0], batch=background_batch)

audio_player = pyglet.media.Player()
audio_player.volume = 0.1
audio_player.loop = True
audio_player.queue(intro)

font_manager = Font(64, 64, main_window.width, main_window.height, main_batch)
# font_manager.write('Level 1', 0, main_window.height-64)

highlight_color = 'purple'
player = Player(img=ball_image, 
                x=main_window.width//2, 
                y=main_window.height//2,
                batch=main_batch)
player_controls = [key.Q, key.W, key.E, key.A, key.S, key.D]
board = HexBoard(radius=32, 
                grid_size=8, 
                origin_x=main_window.width//2, 
                origin_y=main_window.height//2, 
                batch=background_batch,
                player=player)

clock = pyglet.clock.get_default()
clock.schedule_interval_soft(board.fade_tile, 0.005)


@main_window.event
def on_key_press(symbol, modifiers):
    if audio_player.playing == False:
        audio_player.play()
        
    if symbol == key.P:
        screenshot_name = f'screenshot {datetime.datetime.now().strftime('%a %m-%d-%Y %H:%M')}.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
    
    if symbol in player_controls and player.movable():
        """ Note: Axes are flipped and not in the intuitive orientation. """
        if symbol == key.Q:
            board.move_player('UP_LEFT')
        if symbol == key.W:
            board.move_player('UP')
        if symbol == key.E:
            board.move_player('UP_RIGHT')
        if symbol == key.A:
            board.move_player('DOWN_LEFT')
        if symbol == key.S:
            board.move_player('DOWN')
        if symbol == key.D:
            board.move_player('DOWN_RIGHT')
        clock.schedule(player.move)
    
@main_window.event
def on_draw():
    main_window.clear()
    background_batch.draw()
    main_batch.draw()
    
if __name__ == '__main__':
    pyglet.app.run()