import datetime
import time
from collections import namedtuple

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from board import HexBoard
from player import Player
from resources import palette, hex_icon, ball_image, intro, fade_out
from display import WaypointDisplay, ControlDisplay, LevelStartScreen

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


class Hexscape(pyglet.window.Window):
    def __init__(self):
        super().__init__()
        self.set_fullscreen(True)
        self.set_icon(hex_icon)
        self.set_caption('hexscape')
        self.register_event_type('on_level_start')
        self.register_event_type('on_waypoint_discovered')
        self.register_event_type('on_point_scored')
        self.register_event_type('on_menu')
        self.register_event_type('on_game_over')
        
        self.pause_batch = pyglet.graphics.Batch()
        self.background_batch = pyglet.graphics.Batch()
        self.font_group = pyglet.graphics.Group(order=3)
        self.main_batch = pyglet.graphics.Batch()
        self.background_color = pyglet.shapes.Rectangle(0, 0, self.width, self.height, color=palette['black'][0], batch=self.background_batch)

        self.clock = pyglet.clock.get_default()
        self.audio_player = pyglet.media.Player()
        self.audio_player.volume = 0.1
        self.audio_player.loop = True
        self.audio_player.queue(intro)

        self.player = Player(img=ball_image, x=self.width//2, y=self.height//2, batch=self.main_batch)
        self.player_movement_controls = [key.Q, key.W, key.E, key.A, key.S, key.D]
        self.player_action_controls = [key.R]

        self.pause = False
        self.level = 0
        self.board = HexBoard(radius=64, grid_size=4, origin_x=self.width//2, origin_y=self.height//2, batch=self.background_batch,player=self.player,window=self) 
        
        self.hud_label = pyglet.text.Label('', font_size=48, x=10, y=10, font_name='monogram', batch=self.main_batch, group=self.font_group)
        self.level_label = pyglet.text.Label(f'Mission {self.level}', font_size=48, x=10, y=self.height-10, anchor_y='top', font_name='monogram', batch=self.main_batch, group=self.font_group)
        self.waypoint_display = WaypointDisplay(world_x=10, world_y=36, batch=self.main_batch)
        
    def fade_text(self, dt: float, label: pyglet.text.Label):
        label.color = (label.color[0], label.color[1], label.color[2], label.color[3]-8)

    def on_show(self):
        self.dispatch_event('on_level_start', 1)
        
    def on_level_start(self, level: int):
        self.level = level
        self.pause = True
        self.overlay = LevelStartScreen(background_color=palette['black'][0], level=level, screen_width=self.width, screen_height=self.height, batch=self.pause_batch)
        self.level_label.text = f'Mission {self.level}'

    def on_key_press(self, symbol, modifiers):
        if self.pause:
            self.clock.schedule_interval_soft(self.board.fade_tile, 0.005)
            self.pause = False
        
        if self.audio_player.playing == False:
            self.audio_player.play()
            
        if symbol == key.P:
            screenshot_name = f'screenshot {datetime.datetime.now().strftime('%a %m-%d-%Y %H:%M')}.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_name)
        
        if symbol in self.player_movement_controls and self.player.movable():
            if symbol == key.Q:
                self.board.move_player('UP_LEFT')
            if symbol == key.W:
                self.board.move_player('UP')
            if symbol == key.E:
                self.board.move_player('UP_RIGHT')
            if symbol == key.A:
                self.board.move_player('DOWN_LEFT')
            if symbol == key.S:
                self.board.move_player('DOWN')
            if symbol == key.D:
                self.board.move_player('DOWN_RIGHT')
            self.clock.schedule(self.player.move)
        
        if symbol == key.TAB:
            self.waypoint_display.move_select()

    def on_waypoint_discovered(self, color: tuple[int], ability_description: str):
        self.hud_label.color = color
        self.hud_label.text = ability_description.upper()
        self.clock.schedule_interval_for_duration(self.fade_text, 0.5, 20.0, label=self.hud_label)

    def on_draw(self):
        self.clear()
        if self.pause:
            self.pause_batch.draw()
        else:
            self.background_batch.draw()
            self.main_batch.draw()
        
        
if __name__ == '__main__':
    game = Hexscape()
    pyglet.app.run()