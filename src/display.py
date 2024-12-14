import pyglet
from pyglet.text.layout import TextLayout
from pyglet.text.document import InlineElement

from player import Player
from resources import empty_hud_waypoint, palette, arrow_icons


class LevelStartScreen:
    def __init__(self, background_color: tuple[int], level: int, screen_width: int, screen_height: int, batch: pyglet.graphics.Batch) -> None:
        self.background = pyglet.shapes.Rectangle(x=0, y=0, 
                                                  width=screen_width, height=screen_height,
                                                  color=background_color,
                                                  batch=batch, group=pyglet.graphics.Group(order=0))
        self.level_label = pyglet.text.Label(text=f'-- Welcome to Mission {level} --',
                                             x=screen_width//2, y=screen_height//2,
                                             anchor_x='center', anchor_y='center',
                                             font_name='monogram', font_size=64,
                                             batch=batch, group=pyglet.graphics.Group(order=1))
        self.instruction_label = pyglet.text.Label(text='[press any key]',
                                                   x=screen_width//2, y=(screen_height//2)-64,
                                                   anchor_x='center', anchor_y='center',
                                                   font_name='monogram', font_size=40,
                                                   color=(200, 200, 200, 0),  
                                                   batch=batch)
        pyglet.clock.schedule_interval(self.fade_label, 0.025, amount=1)
        
    def fade_label(self, dt: float, amount: int):
        if self.level_label.opacity > 0:
            self.level_label.opacity -= amount
            self.instruction_label.opacity += amount
        else:
            self.level_label.text = ''
            pyglet.clock.unschedule(self.fade_label)
            pyglet.clock.schedule_interval(self.fade_background, 0.01, amount=5)
            
    def fade_background(self, dt: float, amount: int):
        if self.background.opacity > 5:
            self.instruction_label.opacity -= amount
        else:
            pyglet.clock.unschedule(self.fade_background)
        
        
class WaypointDisplay:
    def __init__(self, world_x: int, world_y: int, batch: pyglet.graphics.Batch):
        super().__init__()
        
        keys = ['purple', 'blue', 'green', 'yellow', 'orange', 'red']
        self.selection_boxes = { k: pyglet.shapes.BorderedRectangle(x=world_x, y=world_y+(i*32), 
                                                          width=32, height=32, border=4, 
                                                          color=palette[k][1], border_color=palette[k][0], 
                                                          batch=batch) for i, k in enumerate(keys) }
        
    def select(self, waypoint_color: str):
        self.selection_boxes[waypoint_color].border_color = (self.selection_boxes[waypoint_color].border_color[0], 
                                                             self.selection_boxes[waypoint_color].border_color[1], 
                                                             self.selection_boxes[waypoint_color].border_color[2], 
                                                             255)
    
    
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
        
        self.player_controls_label = pyglet.text.DocumentLabel(document=player_controls,
                                                               anchor_x='right', anchor_y='top',
                                                               width=firstline_width,
                                                               x=screen_width-border, y=screen_height-border, 
                                                               multiline=True, batch=batch, group=group)
        self.player_controls_label.font_name = 'monogram'
        self.player_controls_label.font_size = 30
        self.player_controls_label.color = (255, 255, 255, 255)