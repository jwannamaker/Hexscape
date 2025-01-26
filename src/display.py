import logging

import pyglet
from pyglet.text.layout import TextLayout
from pyglet.text.document import InlineElement

from hex import HexOrientation as hex_util
from player import Player
from resources import empty_hud_waypoint, palette, arrow_icons




class DisplayElement(pyglet.text.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.global_border = 20
        

class LevelStartScreen:
    def __init__(self, background_color: tuple[int], level: int, screen_width: int, screen_height: int, batch: pyglet.graphics.Batch) -> None:
        self.background = pyglet.shapes.Rectangle(x=0, y=0, width=screen_width, height=screen_height, color=background_color, batch=batch, group=pyglet.graphics.Group(order=0))
        self.level_label = pyglet.text.Label(text=f'-- Welcome to Mission {level} --', x=screen_width//2, y=screen_height//2, anchor_x='center', anchor_y='center', font_name='monogram', font_size=64, batch=batch, group=pyglet.graphics.Group(order=1))
        self.instruction_label = pyglet.text.Label(text='[press any key]', x=screen_width//2, y=(screen_height//2)-64, anchor_x='center', anchor_y='center', font_name='monogram', font_size=40, color=(200, 200, 200, 0),   batch=batch)
        pyglet.clock.schedule_interval(self.fade_label, 0.025, amount=1)
        
    def fade_label(self, dt: float, amount: int):
        if self.instruction_label.opacity < 255:
            self.instruction_label.opacity += amount
        else:
            self.instruction_label.opacity = 255
            pyglet.clock.unschedule(self.fade_label)
        

class MoveCountDisplay:
    def __init__(self, world_x: int, world_y: int, batch: pyglet.graphics.Batch):
        back = pyglet.graphics.Group(order=0)
        front = pyglet.graphics.Group(order=1)
        
        self.count = 0
        self.count_label = pyglet.text.Label(self.count, x=world_x, y=world_y, anchor_x='right')

     
class WaypointDisplay:
    def __init__(self, world_x: int, world_y: int, batch: pyglet.graphics.Batch):
        radius = 32
        
        far_back = pyglet.graphics.Group(order=0)
        back = pyglet.graphics.Group(order=1)
        front = pyglet.graphics.Group(order=2)
        
        self.selected_color_index = 0
        self.keys = ['purple', 'blue', 'green', 'yellow', 'orange', 'red']
        self.selection_ring = pyglet.shapes.Polygon(*hex_util.corners(radius+4, world_x+radius, world_y+radius), color=palette['white'][0], batch=batch, group=far_back)
        self.icon_polygons = {k: pyglet.shapes.Polygon(*hex_util.corners(radius, world_x+radius, world_y+(i*2*radius)+radius), color=palette[k][1], batch=batch, group=back) for i, k in enumerate(self.keys)}
        self.inner_polygons = {k: pyglet.shapes.Polygon(*hex_util.corners(radius, world_x+radius, world_y+(i*2*radius)+radius), color=palette['black'][0], batch=batch, group=front) for i, k in enumerate(self.keys)}
        
        self.selection_ring.opacity = 0
        for icon in self.icon_polygons.values():
            icon.opacity = 0
        
    def move_select(self):
        self.selected_color_index = (self.selected_color_index + 1) % len(self.keys)
        self.selection_ring.position = self.icon_polygons[self.keys[self.selected_color_index]].position
    
    def show_collected(self, waypoint_color: str):
        self.icon_polygons[waypoint_color.lower()].opacity = 255
    
    
class ControlDisplay:
    def __init__(self, screen_width: int, screen_height: int, border: int, 
                 batch: pyglet.graphics.Batch, group: pyglet.graphics.Group):
        self.mono_font = pyglet.font.load('monogram', stretch=True)
        
        player_controls = pyglet.text.document.FormattedDocument('CONTROLS')
        self.player_controls_label = pyglet.text.DocumentLabel(player_controls)
        firstline_width = (self.player_controls_label.content_width*1.2)//1
        
        player_controls.append_text('\n[Q]')
        player_controls.insert_element(len(player_controls.text), arrow_icons['up_left'])
        player_controls.append_text('\n[W]')
        player_controls.insert_element(len(player_controls.text), arrow_icons['up'])
        player_controls.append_text('\n[E]')
        player_controls.insert_element(len(player_controls.text), arrow_icons['up_right'])
        player_controls.append_text('\n[A]')
        player_controls.insert_element(len(player_controls.text), arrow_icons['down_left'])
        player_controls.append_text('\n[S]')
        player_controls.insert_element(len(player_controls.text), arrow_icons['down'])
        player_controls.append_text('\n[D]')
        player_controls.insert_element(len(player_controls.text), arrow_icons['down_right'])
        
        self.player_controls_label = pyglet.text.DocumentLabel(document=player_controls, anchor_x='right', anchor_y='top', width=firstline_width, x=screen_width-border, y=screen_height-border,  multiline=True, batch=batch, group=group)
        self.player_controls_label.font_name = 'monogram'
        self.player_controls_label.font_size = 30
        self.player_controls_label.color = (255, 255, 255, 255)