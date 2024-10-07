import pyglet

import resources


class Font:
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
        x, y = max(self.min_x, start_x), max(self.min_y, start_y)
        for char in text:
            if char != ' ':
                letter_img = resources.font[char.upper()]
                letter_sprite = pyglet.sprite.Sprite(img=letter_img, x=x, y=y, batch=self.batch)
                letter_sprite.scale_x = self.size_x / letter_sprite.width
                letter_sprite.scale_y = self.size_y / letter_sprite.height
                
                self.text.append(letter_sprite)
                self.border_boxes.append(pyglet.shapes.Box(x, y, self.size_x, self.size_y, 
                                                           color=(0, 0, 0, 0), batch=self.batch))
            if x + self.size_x <= self.max_x:
                x += self.size_x
            else:
                x = self.min_x
                y += -self.size_y # increment to lower row