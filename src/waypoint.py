import abc
import random
import enum

import pyglet

from resources import palette

    
class WaypointType(enum.Enum):
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    PURPLE = 5
    
    
class Waypoint:
    __data = {
        WaypointType.RED: {
            'color': palette['red'][1],
            'ability_description': 'Break through walls temporarily',
            'duration': 5,
            'rarity': 0.2
        },
        WaypointType.ORANGE: {
            'color': palette['orange'][1],
            'ability_description': 'Light up the path to an undiscovered waypoint',
            'duration': 3,
            'rarity': 0.2
        },
        WaypointType.YELLOW: {
            'color': palette['yellow'][1],
            'ability_description': 'Illuminate all adjacent walls temporarily',
            'duration': 6,
            'rarity': 0.4
        },
        WaypointType.GREEN: {
            'color': palette['green'][1],
            'ability_description': 'Highlight undiscovered waypoints temporarily',
            'duration': 8,
            'rarity': 0.5
        },
        WaypointType.BLUE: {
            'color': palette['blue'][1],
            'ability_description': 'Boost each move to max distance temporarily',
            'duration': 4,
            'rarity': 0.1
        },
        WaypointType.PURPLE: {
            'color': palette['purple'][1],
            'ability_description': 'Teleport to an undiscovered waypoint',
            'duration': 1,
            'rarity': 0.1
        }
    }
    
    def __init__(self, type: WaypointType):
        self.data = Waypoint.__data[type]
        self.activated = False
        
    def activate(self, func: callable):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(func, self.data['duration'])