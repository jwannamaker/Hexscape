from collections import deque

import pyglet
import numpy as np

from waypoint import Waypoint, RedWaypoint, OrangeWaypoint, YellowWaypoint, PurpleWaypoint, GreenWaypoint, BlueWaypoint


class Player(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.Texture, x: int, y: int, 
                 batch: pyglet.graphics.Batch):
        super().__init__(img, x, y, batch=batch)
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        self.next_position = deque([])
        self._movable = True
        
        self.waypoint_collection = {}
        self.timers = deque(maxlen=1)
    
    def movable(self):
        return self._movable
    
    def move(self, dt):
        """ Address the way a player moves according to waypoints activated. """
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        destination = self.current_position if len(self.next_position) == 0 else self.next_position[0]
        distance = self.current_position.distance(destination)
        if distance > 1:
            self._movable = False
            self.x += ((destination[0] - self.x) / distance) * dt * 100
            self.y += ((destination[1] - self.y) / distance) * dt * 100
        else:
            self._movable = True
            if len(self.next_position) > 0:
                self.next_position.popleft()
            pyglet.clock.unschedule(self.move)
        
    def add_next_position(self, screen_position):
        position = pyglet.math.Vec2(*screen_position)
        if position not in self.next_position:
            self.next_position.append(pyglet.math.Vec2(*screen_position))
    
    def collect_waypoint(self, waypoint: Waypoint):
        self.waypoint_collection[waypoint.color()] = waypoint
    
    def activate_waypoint(self, color: str):
        if color in self.waypoint_collection and color not in self.timers:
            self.waypoint_collection[color].activate()
            if isinstance(self.waypoint_collection[color], RedWaypoint):
                """ Toggle something that changes the way the player moves """
                pass
            
    def actionable(self):
        return len(self.waypoint_collection)