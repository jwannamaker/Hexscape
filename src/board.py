import random
from collections import deque

import numpy as np
import pyglet
import pyglet.event

from cell import HexCell
from hex import Hex
from hex import HexOrientation as hex_util
from hex import generate_square_grid
from waypoint import WaypointType, Waypoint
from player import Player
from resources import click_sound, fade_out, ball_image


class HexBoard:
    """ 
    radius:     pixel measurement of radius for a hex tile
    grid_size:  int for creating a 'square' hex grid (each side length matches 
                this)
    """
    def __init__(self, radius: int, grid_size: int, origin_x: int, origin_y: int,
                 batch: pyglet.graphics.Batch, player: Player, window: pyglet.window):
        self._radius = radius
        self._grid_size = grid_size
        self._origin = np.row_stack([origin_x, origin_y])
        self._batch = batch
        self._window = window
        
        self.player_pos = Hex(0, 0, 0)
        self.player = player
        self._player_trail = dict()
        self._player_trail[self.player_pos] = 0
        self._hit_walls = []
        
        self._tiles = {coordinate: HexCell(coordinate, self._radius, self._origin, 'white', self._batch) for coordinate in generate_square_grid(self._grid_size)}
        self._tiles[self.player_pos].highlight()
        
        self.start_level(1)

    def __contains__(self, key: Hex):
        return key in self._tiles
    
    def start_level(self, level: int):
        waypoints = [Waypoint(type) for type in WaypointType]
        weights = [w.data['spawn_frequency'] for w in waypoints]
        place_these_waypoints = deque(random.choices(waypoints, weights, k=random.randint(level + 1, level + 3)))
        
        self.waypoint_graph = {distance: [] for distance in range(1, self._grid_size + 1)}
        while place_these_waypoints:
            current_waypoint = place_these_waypoints.pop()
            
            max_radius = self._grid_size // 2
            half_radius = max_radius // 2
            near_radius = random.randint(1, half_radius)
            far_radius = random.randint(half_radius, max_radius)
            
            rand_pos = Hex(0, 0, 0)
            if current_waypoint.data['spawn_frequency'] > 1:
                self.waypoint_graph[near_radius].append(current_waypoint)
                rand_pos = random.choice(hex_util.ring(Hex(0, 0, 0), near_radius))
            else:
                self.waypoint_graph[far_radius].append(current_waypoint)
                rand_pos = random.choice(hex_util.ring(Hex(0, 0, 0), far_radius))
            
            if not self._tiles[rand_pos].waypoint():
                self._tiles[rand_pos].place_waypoint(current_waypoint)
        
        self.generate_maze_ver1(self._tiles[self.player_pos])
            
    def boundary_check(self, pre_move: Hex, direction: str):
        post_move = hex_util.neighbor(pre_move, direction)
        if post_move in self._tiles:
            if not self._tiles[post_move].walls[pre_move]:
                return post_move
        # Show what's blocking the way
        new_wall_sprite = self._tiles[pre_move].wall_sprite(direction, self._batch)
        self._hit_walls.append(new_wall_sprite)
        return pre_move 

    def fade_tile(self, dt: float):
        for tile, time in list(self._player_trail.items()):
            self._player_trail[tile] += 1 if time < len(fade_out) - 1 else 0
            self._tiles[tile].fade(fade_out[time])    

    def move_player(self, direction: str):
        click_sound.play()
        self.player_pos = self.boundary_check(self.player_pos, direction)
        self._tiles[self.player_pos].highlight()
        
        potential_waypoint = self._tiles[self.player_pos].waypoint()
        if isinstance(potential_waypoint, Waypoint) and potential_waypoint not in self.player.waypoint_collection.values():
            self.player.collect_waypoint(potential_waypoint)
            self._window.dispatch_event('on_waypoint_discovered', potential_waypoint.color(), potential_waypoint.ability_description())
            self._tiles[self.player_pos].remove_waypoint()
        
        next_position = hex_util.center(self.player_pos, self._radius, self._origin)
        self.player.add_next_position(next_position) # smooths player movement
        self._player_trail[self.player_pos] = 0
    
    def remove_wall(self, cell_a: HexCell, cell_b: HexCell):
        if cell_a.coordinate() in cell_b.walls:
            cell_b.remove_wall(cell_a)
        if cell_b.coordinate() in cell_a.walls:
            cell_a.remove_wall(cell_b)
    
    def add_wall(self, cell_a: HexCell, cell_b: HexCell):
        if cell_a.coordinate() in cell_b.walls:
            cell_b.add_wall(cell_a)
        if cell_b.coordinate() in cell_a.walls:
            cell_a.add_wall(cell_b)
    
    def unvisited_neighbors(self, tile: HexCell):
        neighbors = hex_util.neighbors(tile.coordinate())
        return [self._tiles[neighbor] for neighbor in neighbors if neighbor in self._tiles and self._tiles[neighbor].unvisited()]
    
    def generate_maze_ver1(self, current_tile: HexCell):
        if current_tile.unvisited():
            current_tile.visit()
        
        neighbors = self.unvisited_neighbors(current_tile)
        random.shuffle(neighbors)
    
        for potential_neighbor in neighbors:
            if potential_neighbor.coordinate() in self._tiles:
                neighbor_tile = self._tiles[potential_neighbor.coordinate()]
                
                if neighbor_tile.unvisited():
                    self.remove_wall(current_tile, neighbor_tile)
                    self.generate_maze_ver1(neighbor_tile)
                    
    def generate_maze_ver2(self, current_tile: HexCell):
        self.generate_maze_ver1(current_tile)
        self.apply_sparseness(probability=10, percent_fill=75)
    
    def tile_count(self):
        return len(self._tiles.values())
    
    def fill(self):
        fill = 100
        percent = self.tile_count() // 100
        for tile in self._tiles:
            if self._tiles[tile].blocked_off():
                fill -= percent
        return fill

    def apply_sparseness(self, *, probability: int, percent_fill: int):
        
        while self.fill() > percent_fill:
            for tile, cell_a in self._tiles.items():
                if len(list(filter(None, cell_a.walls))) == 5:
                    if random.randint(1, 100) <= probability:
                        self.add_wall(tile, tile)
                        
if __name__ == '__main__':
    test_window = pyglet.window.Window()
    test_batch = pyglet.graphics.Batch()
    test_player = Player(ball_image, test_window.width//2, test_window.height//2, test_batch)
    test_board = HexBoard(radius=64, grid_size=4, origin_x=test_window.width//2, origin_y=test_window.height//2, batch=test_batch,player=test_player,window=test_window)
    
    print(f'tile_count: {test_board.tile_count()}')
    print(f'fill: {test_board.fill()}')