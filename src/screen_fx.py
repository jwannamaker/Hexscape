import pyglet


class LevelStartScreen:
    def __init__(self, background_color: tuple[int], level: int, screen_width: int, screen_height: int, 
                 batch: pyglet.graphics.Batch) -> None:
        
        self.background = pyglet.shapes.Rectangle(0, 0, screen_width, screen_height,
                                                  color=background_color,
                                                  batch=batch, group=pyglet.graphics.Group(order=0))
        self.level_label = pyglet.text.Label(text=f'Welcome to Mission {level}',
                                             anchor_x='center', anchor_y='center',
                                             font_name='monagram', font_size=48,
                                             batch=batch, group=pyglet.graphics.Group(order=1))
        
    def fade(self, amount: int):
        self.background.opacity -= amount
        self.level_label.opacity -= amount