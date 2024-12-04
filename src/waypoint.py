import abc
import random

import pyglet

from resources import palette



waypoint = {
    'RED': {
        'color': palette['red'][1],
        'ability_description': 'Break through walls temporarily',
        'duration': 10
    },
    'ORANGE': {
        'color': palette['orange'][1],
        'ability_description': 'Light up the path to an undiscovered waypoint',
        'duration': 3
    },
    'YELLOW': {
        'color': palette['yellow'][1],
        'ability_description': 'Illuminate all adjacent walls temporarily',
        'duration': 10
    },
    'GREEN': {
        'color': palette['green'][1],
        'ability_description': 'Highlight the other waypoints temporarily',
        'duration': 10
    },
    'BLUE': {
        'color': palette['blue'][1],
        'ability_description': 'Boost each move to max distance temporarily',
        'duration': 12
    },
    'PURPLE': {
        'color': palette['purple'][1],
        'ability_description': 'Teleport to an undiscovered waypoint',
        'duration': 1
    }
}
