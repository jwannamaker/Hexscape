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
            'rarity': 0.2
        },
        WaypointType.ORANGE: {
            'color': palette['orange'][1],
            'ability_description': 'Light up the path to an undiscovered waypoint',
            'duration': 3,
            'rarity': 0.7
        },
        WaypointType.YELLOW: {
            'color': palette['yellow'][1],
            'ability_description': 'Illuminate all adjacent walls temporarily',
            'duration': 6,
            'rarity': 0.9
        },
        WaypointType.GREEN: {
            'color': palette['green'][1],
            'ability_description': 'Highlight undiscovered waypoints temporarily',
            'duration': 8,
            'rarity': 1.0
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
            'rarity': 0.2
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
        print(f'{l.data['rarity']}\t {l.data['ability_description']}')  
        
if __name__ == '__main__':
    radius = 6
    potential_waypoints = [Waypoint(type) for type in WaypointType]
    for level in range(1, 10):
        place_these_waypoints = sorted(deque(random.choices(potential_waypoints,
                                        [w.data['rarity'] for w in potential_waypoints], 
                                        k=random.randint(level, level+random.randint(1, 3)))),
                                        key=lambda w: w.data['rarity'])
        
        print(f'---- LEVEL {level} -----')
        print_list(place_these_waypoints)
        
        waypoint_graph = {distance: deque(maxlen=distance) for distance in range(1, radius+1)}
        # while len(place_these_waypoints) > 0:
        #     distance = random.randint(1, radius)
            
        #     if len(waypoint_graph[distance]) == 0: # check if there are waypoints this far away
        #         waypoint_graph[distance].append(place_these_waypoints.pop()) 
        #         # place the waypoint so it's sorted in ascending rarity
        #         # i.e. lower rarity --> HIGHER RARITY
        
        print(waypoint_graph)
        
        print()
        print()
        
        # TODO make sure there are limits on how many of one single type of waypoint spawns