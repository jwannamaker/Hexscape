import string

import pyglet


class Font:
    char_list = [
        '5', '6', '7', '8', '9', '0',
        'Y', 'Z', '1', '2', '3', '4',
        'S', 'T', 'U', 'V', 'W', 'X',
        'M', 'N', 'O', 'P', 'Q', 'R',
        'G', 'H', 'I', 'J', 'K', 'L',
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    
    def __init__(self, window_width, window_height, batch):
        self.text = []
        self.min_x = 0
        self.min_y = 0
        self.max_x = window_width - 128
        self.max_y = window_height - 128
        self.batch = batch
    
    def write(self, text, start_x, start_y, group=None):
        x, y = start_x, start_y
        for char in text:
            if char != ' ':
                self.text.append(pyglet.sprite.Sprite(img=pyglet.resource.image(f'{char.upper()}.png'),
                                                    x=x, y=y, batch=self.batch))
            if x + 128 <= self.max_x:
                x += 128
            else:
                x = self.min_x
                y += -128