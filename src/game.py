import datetime
import time
from collections import namedtuple

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from board import HexBoard
from cell import HexCell
from player import Player
from resources import palette, hex_icon, ball_image, intro, fade_out
from display import WaypointDisplay, ControlDisplay

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

main_window = pyglet.window.Window()
main_window.set_fullscreen(True)
main_window.set_icon(hex_icon)
main_window.set_caption('hexscape')
main_window.register_event_type('on_waypoint_discovered')
main_window.register_event_type('on_point_scored')
main_window.register_event_type('on_next_level')
main_window.register_event_type('on_game_over')
main_window.register_event_type('on_menu')


background_batch = pyglet.graphics.Batch()
font_group = pyglet.graphics.Group(order=3)
main_batch = pyglet.graphics.Batch()
background_color = pyglet.shapes.Rectangle(0, 0, main_window.width, main_window.height,
                                           color=palette['black'][0], batch=background_batch)


audio_player = pyglet.media.Player()
audio_player.volume = 0.1
audio_player.loop = True
audio_player.queue(intro)


player = Player(img=ball_image, 
                x=main_window.width//2, 
                y=main_window.height//2,
                batch=main_batch)
player_movement_controls = [key.Q, key.W, key.E, key.A, key.S, key.D]
player_action_controls = [key.R]

def fade_text(dt: float, label: pyglet.text.Label):
    label.color = (label.color[0], label.color[1], label.color[2], label.color[3]-8)
    
# hud = ControlDisplay(main_window.width, main_window.height, 10, main_batch, font_group)
hud_label = pyglet.text.Label('', font_size=48, x=10, y=10, font_name='monogram', 
                              batch=main_batch, group=font_group)
level_label = pyglet.text.Label('LEVEL 1', font_size=48, x=10, y=main_window.height-10, 
                                anchor_y='top', font_name='monogram', 
                                batch=main_batch, group=font_group)
waypoint_label = WaypointDisplay(main_batch)


board = HexBoard(radius=64, 
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

@main_window.event
def on_waypoint_discovered(color: tuple[int], ability_description: str):
    hud_label.color = color
    hud_label.text = ability_description.upper()
    clock.schedule_interval_for_duration(fade_text, 0.5, 20.0, label=hud_label)

@main_window.event
def on_draw():
    main_window.clear()
    background_batch.draw()
    main_batch.draw()
    
if __name__ == '__main__':
    print(main_window.event_types)
    print(f'user font loaded: {pyglet.font.have_font('pixelator')}')
    pyglet.app.run()