import logging
from collections import deque

import pyglet
import numpy as np

from waypoint import Waypoint, WaypointType

logging.basicConfig(filename='player.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Player(pyglet.sprite.Sprite):
    def __init__(self, img: pyglet.image.Texture, x: int, y: int, batch: pyglet.graphics.Batch):
        super().__init__(img, x, y, batch=batch)
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        self.next_position = deque([])
        self._movable = True
        
        self.waypoint_collection : dict[WaypointType, Waypoint] = {}
        self.active_waypoints : deque[WaypointType] = deque()
    
    def movable(self):
        return self._movable
    
    def move(self, dt):
        self.current_position = pyglet.math.Vec2(self.x, self.y)
        destination = self.current_position if len(self.next_position) == 0 else self.next_position[0]
        distance = self.current_position.distance(destination)
        if distance > 1:
            self._movable = False
            self.x += ((destination[0] - self.x) / distance) * dt * 150
            self.y += ((destination[1] - self.y) / distance) * dt * 150
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
        if waypoint.type in self.waypoint_collection:
            logger.log(logging.DEBUG, f'Player already has {waypoint.color_name()} waypoint. Not collected.')
        else:
            self.waypoint_collection[waypoint.type] = waypoint

            logger.log(logging.DEBUG, f'Player collected {waypoint.color_name()} waypoint')
            logger.log(logging.DEBUG, f'Player waypoint collection update: {self.waypoint_collection}')
    
    def activate_waypoint(self,  waypoint_type: WaypointType):
        if waypoint_type in self.waypoint_collection and waypoint_type not in self.active_waypoints:
            self.waypoint_collection[waypoint_type].activate()
            self.active_waypoints.append(waypoint_type)
    
    def actionable(self):
        actionable = False
        for color in self.waypoint_collection:
            if not self.waypoint_collection[color].activated:
                actionable = True
        return actionable