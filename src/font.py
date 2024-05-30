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
    
    def __init__(self, size_x, size_y, window_width, window_height, batch):
        self.text = []
        self.size_x = size_x
        self.size_y = size_y
        self.border_boxes = []
        
        self.min_x = 0
        self.min_y = 0
        self.max_x = window_width - size_x
        self.max_y = window_height - size_y
        self.batch = batch
    
    def write(self, text, start_x, start_y):
        x, y = start_x, start_y
        for char in text:
            if char != ' ':
                letter_img = pyglet.resource.image(f'{char.upper()}.png')
                letter_sprite = pyglet.sprite.Sprite(img=letter_img, x=x, y=y, batch=self.batch)
                letter_sprite.scale_x = self.size_x / letter_sprite.width
                
                self.text.append(letter_sprite)
                self.border_boxes.append(pyglet.shapes.Box(x, y, self.size_x, self.size_y, 
                                                           5, batch=self.batch))
            if x + self.size_x <= self.max_x:
                x += self.size_x
            else:
                x = self.min_x
                y += -self.size_y # increment to lower row