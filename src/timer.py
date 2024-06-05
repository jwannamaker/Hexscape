import pyglet

class Timer:
    def __init__(self, x_pos, y_pos, batch):
        self.label = pyglet.text.Label('00:00', font_size=128, 
                                       x=x_pos, y=y_pos, batch=batch,
                                       anchor_x='right', anchor_y='top')
        self.reset()

    def start(self):
        self.running = True


    
    def reset(self):
        self.time = 0
        self.running = False
        self.label.text = '00:00'
        self.label.color = (200, 200, 200, 100)

    def update(self, dt):
        if self.running:
            self.time += dt
            m, s = divmod(self.time, 60)
            self.label.text = f'{round(m):02}:{round(s):02}'
            if s >= 15:
                self.label.color = (215, 210, 215, 150)
            elif s >= 30: 
                self.label.color = (230, 220, 230, 175)
            