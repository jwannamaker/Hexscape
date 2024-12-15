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
    radius = 6
    potential_waypoints = [Waypoint(type) for type in WaypointType]
    for level in range(1, 10):
        place_these_waypoints = sorted(deque(random.choices(potential_waypoints, [w.data['spawn_frequency'] for w in potential_waypoints], 
                                                            k=random.randint(level+1, level+random.randint(2, 3)))),
                                                            key=lambda w: w.data['spawn_frequency'])
        
        waypoint_graph = {distance: deque() for distance in range(1, radius+1)}
        while len(place_these_waypoints) > 0:
            nearby = random.randint(1, radius//2)
            far = random.randint(radius//2, radius)
            
            current_waypoint = place_these_waypoints.pop()
            if current_waypoint.data['spawn_frequency'] > 1:
                waypoint_graph[nearby].append(current_waypoint)
            else:
                waypoint_graph[far].append(current_waypoint)
        
        print(f'---- LEVEL {level} -----')
        print(waypoint_graph)