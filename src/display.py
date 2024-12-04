import pyglet
from pyglet.text.layout import TextLayout
from pyglet.text.document import InlineElement

from player import Player
from resources import empty_hud_waypoint, palette, arrow_icons

class WaypointDisplay:
    def __init__(self, batch: pyglet.graphics.Batch):
        super().__init__()
        
        keys = ['purple', 'blue', 'green', 'yellow', 'orange', 'red']
        self.boxes = { k: lambda: pyglet.shapes.BorderedRectangle(x=0, y=i*32, width=32, height=32, border=1, color=(255, 0, 0, 255), border_color=(255, 255, 255, 0), batch=batch) for i, k in enumerate(keys) }
        
    def select(self, waypoint_color: str):
        self.boxes[waypoint_color].border_color = (self.boxes[waypoint_color].border_color[0], self.boxes[waypoint_color].border_color[1], self.boxes[waypoint_color].border_color[2], 255)
    
    
class ControlDisplay:
    def __init__(self, screen_width: int, screen_height: int, border: int, 
                 batch: pyglet.graphics.Batch, group: pyglet.graphics.Group):
        self.mono_font = pyglet.font.load('monogram', stretch=True)
        
        player_controls = pyglet.text.document.FormattedDocument('CONTROLS')
        self.player_controls_label = pyglet.text.DocumentLabel(player_controls)
        firstline_width = self.player_controls_label.content_width*1.2//1
        
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
        
        self.player_controls_label = pyglet.text.DocumentLabel(document=player_controls,
                                                               anchor_x='right', anchor_y='top',
                                                               width=firstline_width,
                                                               x=screen_width-border, y=screen_height-border, 
                                                               multiline=True, batch=batch, group=group)
        self.player_controls_label.font_name = 'monogram'
        self.player_controls_label.font_size = 30
        self.player_controls_label.color = (255, 255, 255, 255)