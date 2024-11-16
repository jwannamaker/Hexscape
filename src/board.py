import random

import numpy as np
import pyglet

from cell import HexCell
from hex import Hex
from hex import HexOrientation as hex_util
from hex import generate_square_grid
from player import Player
from resources import click_sound, fade_out


class HexBoard:
    """ 
    radius:     pixel measurement of radius for a hex tile
    grid_size:  int for creating a 'square' hex grid (each side length matches 
                this)
    """
    def __init__(self, radius: int, grid_size: int, origin_x: int, origin_y: int,
                 batch: pyglet.graphics.Batch, player: Player):
        self._radius = radius
        self._grid_size = grid_size
        self._origin = np.row_stack([origin_x, origin_y])
        self._batch = batch
        
        self._tiles = {coordinate: HexCell(coordinate, self._radius, self._origin, 'white', self._batch) 
                       for coordinate in generate_square_grid(self._grid_size)}
        
        self.player_pos = Hex(0, 0, 0)
        self.player = player
        self._player_trail = dict()
        self._player_trail[self.player_pos] = 0
        self._hit_walls = []
        self.highlight_tile(self.player_pos)
        
        self.generate_maze(self._tiles[self.player_pos])

    def __contains__(self, key: Hex):
        return key in self._tiles
            
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
    
    def highlight_tile(self, hex: Hex):
        self._tiles[hex].highlight()

    def move_player(self, direction: str):
        click_sound.play()
        new_tile = self.boundary_check(self.player_pos, direction)
        self.player_pos = new_tile
        self.highlight_tile(self.player_pos)

        next_position = hex_util.center(new_tile, self._radius, self._origin)
        self.player.add_next_position(next_position)
        self._player_trail[new_tile] = 0

    def remove_wall(self, cell_a: HexCell, cell_b: HexCell):
        if cell_a.coordinate() in cell_b.walls:
            cell_b.remove_wall(cell_a)
        if cell_b.coordinate() in cell_a.walls:
            cell_a.remove_wall(cell_b)
    
    def unvisited_neighbors(self, tile: HexCell):
        neighbors = hex_util.neighbors(tile.coordinate())
        return [self._tiles[neighbor] for neighbor in neighbors if neighbor in self._tiles and self._tiles[neighbor].unvisited()]

    def generate_maze(self, current_tile: HexCell):
        if current_tile.unvisited():
            current_tile.visit()
        
        neighbors = self.unvisited_neighbors(current_tile)
        random.shuffle(neighbors)
    
        for potential_neighbor in neighbors:
            if potential_neighbor.coordinate() in self._tiles:
                neighbor_tile = self._tiles[potential_neighbor.coordinate()]
                
                if neighbor_tile.unvisited():
                    self.remove_wall(current_tile, neighbor_tile)
                    self.generate_maze(neighbor_tile)
            
        