import pyglet


class StartScreen:
    def __init__(self, level: int) -> None:
        
        self.level_label = pyglet.text.Label(text=f'Level {level}',
                                             )