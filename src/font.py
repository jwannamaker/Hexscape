import string

import pyglet


class BaseObject(pyglet.sprite.Sprite):
    def __init__(self, texture, *args, **kwargs):
        self.texture = texture
        super().__init__(texture, *args, **kwargs)
        self.color = (255, 255, 255)
        self.opacity = 255

class Font:
    def __init__(self, char, x, y, batch):
        self.char_list = [
            '5', '6', '7', '8', '9', '0',
            'Y', 'Z', '1', '2', '3', '4',
            'S', 'T', 'U', 'V', 'W', 'X',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'G', 'H', 'I', 'J', 'K', 'L',
            'A', 'B', 'C', 'D', 'E', 'F'
        ]
        char = char.upper()
        self.source_image = pyglet.image.load('resources/palace-font.png')
        
        
        self.image_grid = pyglet.image.ImageGrid(self.source_image, rows=6, columns=6)
        self.texture_grid = pyglet.image.TextureGrid(self.image_grid)
        
        index = self.char_list.index(char)
        print(index)
        
        self.sprite = pyglet.sprite.Sprite(img=self.image_grid[index], batch=batch) 
        
        self.sprite.color = (255, 255, 255)
        # self.sprite.opacity = 255
        self.sprite.x = x
        self.sprite.y = y
        # i += 128
        self.sprite.draw()
        self.sprite.image.blit(x, y)
        self.sprite.image.save(f'{char}.png')
    
    def render(self, text, x, y, batch):
        sprites = []
        
        i, j = x, y
        for ch in text:
            char_sprite = pyglet.sprite.Sprite(img=self.image_grid[self.char_list.index(ch)],
                                               x=i, y=j, batch=batch)
            self.spritesprite.append(char_sprite)
            i += self.texture_grid[0].width
            
        return sprites
    
if __name__ == '__main__':
    for ch in string.ascii_uppercase:
        Font(ch, 0, 0, pyglet.graphics.Batch()) 
    for ch in string.digits:
        Font(ch, 0, 0, pyglet.graphics.Batch())