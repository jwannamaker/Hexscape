import pyglet


class StartScreen(pyglet.window.Window):
    def __init__(self, level: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.level_label = pyglet.text.Label(text=f'Level {level}',
                                             )