import datetime
import time
from collections import namedtuple

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from board import HexBoard
from cell import HexCell
from font import Font
from player import Player
from resources import palette, hex_image, ball_image, intro, full_track

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)
main_window.set_icon(hex_image)
main_window.set_caption('hexscape')
main_window.register_event_type('on_waypoint_discovered')


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


player = Player(img=ball_image, 
                x=main_window.width//2, 
                y=main_window.height//2,
                batch=main_batch)
player_movement_controls = [key.Q, key.W, key.E, key.A, key.S, key.D]
player_action_controls = [key.R, key.G]


board = HexBoard(radius=32, 
                 grid_size=4, 
                 origin_x=main_window.width//2, 
                 origin_y=main_window.height//2, 
                 batch=background_batch,
                 player=player,
                 window=main_window)


clock = pyglet.clock.get_default()
clock.schedule_interval_soft(board.fade_tile, 0.005)


@main_window.event
def on_key_press(symbol, modifiers):
    if audio_player.playing == False:
        audio_player.play()
        
    if symbol == key.P:
        screenshot_name = f'screenshot {datetime.datetime.now().strftime('%a %m-%d-%Y %H:%M')}.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
    
    if symbol in player_movement_controls and player.movable():
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
    
    if symbol in player_action_controls and player.actionable():
        if symbol == key.R:
            player.activate_waypoint('red')

@main_window.event
def on_waypoint_discovered(ability_description: str):
    font_manager.write(ability_description, 10, 74)

@main_window.event
def on_draw():
    main_window.clear()
    background_batch.draw()
    main_batch.draw()
    
if __name__ == '__main__':
    print(main_window.event_types)
    pyglet.app.run()