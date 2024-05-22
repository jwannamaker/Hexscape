import pyglet


class Button:
    def __init__(self, window):
        self.buttons = []
        self.window = window
        self.button_img = pyglet.resource.image('base-purple-button-128x64.png')
        self.hover_img = pyglet.resource.image('hover-purple-button-128x64.png')
        self.press_img = pyglet.resource.image('press-purple-button-128x64.png')
        
    def make_button(self, x, y, batch):
        new_button = pyglet.gui.PushButton(x=x, y=y, batch=batch,
                                           pressed=self.button_img, 
                                           hover=self.hover_img, 
                                           depressed=self.press_img)
        self.window.push_handlers(new_button)
        self.buttons.append(new_button)
        
        return new_button
    