import abc
import random
import enum
from collections import deque

import pyglet

from resources import palette

    
class WaypointType(enum.Enum):
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    GREEN = 'green'
    BLUE = 'blue'
    PURPLE = 'purple'

 
class Waypoint:
    __data = {
        WaypointType.RED: {
            'color': palette['red'][1],
            'ability_description': 'Break through walls temporarily',
            'duration': 5,
            'spawn_frequency': 0.2
        },
        WaypointType.ORANGE: {
            'color': palette['orange'][1],
            'ability_description': 'Light up the path to an undiscovered waypoint',
            'duration': 3,
            'spawn_frequency': 0.7
        },
        WaypointType.YELLOW: {
            'color': palette['yellow'][1],
            'ability_description': 'Illuminate all adjacent walls temporarily',
            'duration': 6,
            'spawn_frequency': 0.9
        },
        WaypointType.GREEN: {
            'color': palette['green'][1],
            'ability_description': 'Highlight undiscovered waypoints temporarily',
            'duration': 8,
            'spawn_frequency': 1.0
        },
        WaypointType.BLUE: {
            'color': palette['blue'][1],
            'ability_description': 'Boost each move to max distance temporarily',
            'duration': 4,
            'spawn_frequency': 0.1
        },
        WaypointType.PURPLE: {
            'color': palette['purple'][1],
            'ability_description': 'Teleport to an undiscovered waypoint',
            'duration': 1,
            'spawn_frequency': 0.2
        }
    }
    
    def __repr__(self):
        return self.type.name
    
    def __str__(self):
        return self.type.name
    
    def __init__(self, type: WaypointType):
        self.type = type
        self.data = Waypoint.__data[type]
        self.activated = False
    
    def activate(self, func: callable):
        self.activated = True
        pyglet.clock.schedule_interval_for_duration(func, self.data['duration'])

def print_list(list):
    for l in list:
        print(f'{l.data['spawn_frequency']}\t {l.data['ability_description']}')  


if __name__ == '__main__':
    waypoints = [Waypoint(type) for type in WaypointType]
    print(waypoints)