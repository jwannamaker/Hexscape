import pyglet


class BaseObject(pyglet.sprite.Sprite):
    def __init__(self, texture, *args, **kwargs):
        self.texture = texture
        super().__init__(texture, *args, **kwargs)
        self.color = (255, 255, 255)
        self.opacity = 255

class Font:
    def __init__(self, text, x, y, batch):
        self.char_list = [
            '5', '6', '7', '8', '9', '0',
            'Y', 'Z', '1', '2', '3', '4',
            'S', 'T', 'U', 'V', 'W', 'X',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'G', 'H', 'I', 'J', 'K', 'L',
            'A', 'B', 'C', 'D', 'E', 'F'
        ]
        self.source_image = pyglet.image.load('resources/palace-font.png')
        
        
        self.image_grid = pyglet.image.ImageGrid(self.source_image, rows=6, columns=6)
        self.texture_grid = pyglet.image.TextureGrid(self.image_grid)
        
        indices = [self.char_list.index(i) for i in text]
        print(indices)
        
        self.sprites = [pyglet.sprite.Sprite(img=self.texture_grid[i].get_image_data(), batch=batch) for i in indices]
        for s in self.sprites:
            s.color = (255, 255, 255)
            # s.opacity = 255
            s.x = x
            s.y = y
            # i += 128
            s.draw()
            s.image.blit(x, y)
            s.image.save('letter.png')
    
    def render(self, text, x, y, batch):
        sprites = []
        
        i, j = x, y
        for ch in text:
            char_sprite = pyglet.sprite.Sprite(img=self.image_grid[self.char_list.index(ch)],
                                               x=i, y=j, batch=batch)
            sprites.append(char_sprite)
            i += self.texture_grid[0].width
            
        return sprites