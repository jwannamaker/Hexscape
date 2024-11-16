import abc

from resources import palette


class Waypoint(abc.ABC):
    @abc.classmethod
    def color(self, shade: int):
        raise NotImplementedError

    @abc.abstractmethod
    def ability_description(self):
        raise NotImplementedError

    @abc.abstractmethod
    def duration(self):
        raise NotImplementedError


class RedWaypoint(Waypoint):
    def color(self, shade: int):
        return palette['red'][shade]
    
    def ability_description(self):
        return 'Break through walls temporarily'
    
    def duration(self):
        return 10
    
    
class OrangeWaypoint(Waypoint):
    def color(self, shade: int):
        return palette['orange'][shade]
    
    def ability_description(self):
        return 'Light up a path to the nearest waypoint temporarily'

    def duration(self):
        return 10


class YellowWaypoint(Waypoint):
    def color(self, shade: int):
        return palette['yellow'][shade]
    
    def ability_description(self):
        return 'Light up the surrounding tiles (and walls) temporarily'

    def duration(self):
        return 30


class PurpleWaypoint(Waypoint):
    def color(self, shade: int):
        return palette['purple'][shade]
        
    def ability_description(self):
        return 'Teleport to another waypoint'

    def duration(self):
        return 10


class GreenWaypoint(Waypoint):
    def color(self, shade: int):
        return palette['green'][shade]
    
    def ability_description(self):
        return 'Light up other waypoints temporarily'
    
    def duration(self):
        return 15
