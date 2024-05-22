import string

import pyglet

pyglet.resource.path = ['../resources', '../resources/font']
pyglet.resource.reindex()

class Font:
    char_list = [
        '5', '6', '7', '8', '9', '0',
        'Y', 'Z', '1', '2', '3', '4',
        'S', 'T', 'U', 'V', 'W', 'X',
        'M', 'N', 'O', 'P', 'Q', 'R',
        'G', 'H', 'I', 'J', 'K', 'L',
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    
    def __init__(self, batch):
        self.text = []
        self.batch = batch
    
    def write(self, text, start_x, start_y, batch):
        x, y = start_x, start_y
        for char in text:
            self.text.append(pyglet.sprite.Sprite(img=pyglet.resource.image(f'{char.upper()}.png'),
                                                  x=x, y=y, batch=batch))
            x += 128
            