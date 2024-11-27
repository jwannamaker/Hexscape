import abc
import random

import pyglet

from resources import palette

class Waypoint(abc.ABC):
    def __init__(self):
        self.activated = False
        self.time_remaining = self.duration()
    
    @abc.abstractmethod
    def activate():
        raise NotImplementedError
    
    @abc.abstractmethod
    def color(self, shade=1) -> tuple[int]:
        raise NotImplementedError

    @abc.abstractmethod
    def ability_description(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def duration(self) -> float:
        raise NotImplementedError


class RedWaypoint(Waypoint):
    def __str__(self) -> str:
        return 'red'
    
    def __repr__(self) -> str:
        return 'red_waypoint'
    
    def __init__(self):
        super().__init__()
    
    def countdown(self, dt: float):
        return self.duration() - dt
    
    def activate(self):
        """ Might need to add a parameter to keep reference of the timer used. """
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(self.countdown, 0.1, self.duration())
    
    def color(self, shade=1):
        return palette['red'][shade]
    
    def ability_description(self):
        return 'Break through walls temporarily'
    
    def duration(self):
        return 10.0
    
    
class OrangeWaypoint(Waypoint):
    def __str__(self) -> str:
        return 'orange'
    
    def __repr__(self) -> str:
        return 'orange_waypoint'
    
    def countdown(self, dt: float):
        return self.duration() - dt
    
    def activate(self):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(self.countdown, 0.1, self.duration())
        
    def color(self, shade=1):
        return palette['orange'][shade]
    
    def ability_description(self):
        return 'Light up a path to the nearest waypoint temporarily'

    def duration(self):
        return 10.0


class YellowWaypoint(Waypoint):
    def __str__(self) -> str:
        return 'yellow'
    
    def __repr__(self) -> str:
        return 'yellow_waypoint'
    
    def countdown(self, dt: float):
        return self.duration() - dt
    
    def activate(self):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(self.countdown, 0.1, self.duration())
        
    def color(self, shade=1):
        return palette['yellow'][shade]
    
    def ability_description(self):
        return 'Light up the surrounding tiles (and walls) temporarily'

    def duration(self):
        return 30.0


class PurpleWaypoint(Waypoint):
    def __str__(self) -> str:
        return 'purple'
    
    def __repr__(self) -> str:
        return 'purple_waypoint'
    
    def countdown(self, dt: float):
        return self.duration() - dt
    
    def activate(self):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(self.countdown, 0.1, self.duration())
        
    def color(self, shade=1):
        return palette['purple'][shade]
        
    def ability_description(self):
        return 'Teleport to another waypoint'

    def duration(self):
        return 10.0


class GreenWaypoint(Waypoint):
    def __str__(self) -> str:
        return 'green'
    
    def __repr__(self) -> str:
        return 'green_waypoint'
    
    def countdown(self, dt: float):
        return self.duration() - dt
    
    def activate(self):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(self.countdown, 0.1, self.duration())
        
    def color(self, shade=1):
        return palette['green'][shade]
    
    def ability_description(self):
        return 'Light up other waypoints temporarily'
    
    def duration(self):
        return 15.0
    
    
class BlueWaypoint(Waypoint):
    def __str__(self) -> str:
        return 'blue'
    
    def __repr__(self) -> str:
        return 'blue_waypoint'
    
    def countdown(self, dt: float):
        return self.duration() - dt
    
    def activate(self):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(self.countdown, 0.1, self.duration())
        
    def color(self, shade=1):
        return palette['blue'][shade]
    
    def ability_description(self):
        return 'Every move is the max move possible'
    
    def duration(self):
        return 15.0
