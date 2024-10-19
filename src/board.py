import numpy as np
import pyglet


from hex import Hex, HexOrientation
from player import Player
from resources import bop_laser_sound, click_sound, fade_out, palette


class HexBoard:
    """ 
    radius:     pixel measurement of radius for a hex tile
    grid_size:  int for creating a 'square' hex grid (each side length matches 
                this int)
    origin_x:   x coordinate in pixels for center of origin tile
    origin_y:   y coordinate in pixels for center of origin tile
    batch:      batch that the board is rendered with
    player:     player that gets placed on the board
    clock:      clock from the running app
    """
    def __init__(self, radius: int, grid_size: int, origin_x: int, origin_y: int,
                 batch: pyglet.graphics.Batch, player: Player):
        self._radius = radius
        self._grid_size = grid_size
        self._origin = np.row_stack([origin_x, origin_y])
        self._batch = batch

        self._tiles = {}
        for q in range(-self._grid_size, self._grid_size + 1, 1):
            start_r = max(-self._grid_size, -q - self._grid_size)
            stop_r = min(self._grid_size, -q + self._grid_size)
            for r in range(start_r, stop_r + 1, 1):
                s = -q - r
                new_tile = Hex(q, r, s)
                self._tiles[new_tile] = self.tile(new_tile)

        self.player_pos = Hex(0, 0, 0)
        self.player = player
        self._player_trail = dict()
        self._player_trail[self.player_pos] = 0
        self.highlight_tile(self.player_pos)

    def tile(self, hex: Hex):
        """ Return a dict with entries
            [
                'background': pyglet.shapes.Polygon, 
                'foreground': pyglet.shapes.Polygon
            ]
        corresponding to the tile at hex. """
        center_x, center_y = HexOrientation.center(hex, self._radius, self._origin)
        background = pyglet.shapes.Polygon(*HexOrientation.corners(self._radius, center_x, center_y),
                                           color=palette['blue'][1],
                                           batch=self._batch)
        foreground = pyglet.shapes.Polygon(*HexOrientation.corners(self._radius - 4, center_x, center_y),
                                           color=palette['blue'][0],
                                           batch=self._batch)
        foreground.opacity = 0
        return {'background': background, 'foreground': foreground}

    def nearby(self, hex: Hex, search_distance: int):
        """ Returns a list of hex coordinates within search_distance to the given 
        hex coordinate.
        Note: The coordinates WILL need to be validated by the map.
        """
        results = []
        for q in range(-search_distance, search_distance + 1, 1):
            # Find only the revelvant values for r to iterate over, considering
            # q + r + s == 0
            start_r = max(-search_distance, -q - search_distance)
            stop_r = min(search_distance, -q + search_distance)
            for r in range(start_r, stop_r + 1, 1):
                s = -q - r
                results.append(hex + Hex(q, r, s))
        return results

    def __contains__(self, key: Hex):
        return key in self._tiles

    def boundary_check(self, pre_move: Hex, direction: str):
        post_move = pre_move + HexOrientation.ADJACENT_DIRECTION[direction]
        if post_move.distance_to(Hex(0, 0, 0)) <= self._grid_size:
            return post_move
        bop_laser_sound.play()
        return pre_move

    def fade_tile(self, dt: float):
        for tile, time in list(self._player_trail.items()):
            self._player_trail[tile] += 1 if time < len(fade_out) - 1 else 0
            self._tiles[tile]['foreground'].opacity = fade_out[time]


    def highlight_tile(self, hex: Hex):
        """ Highlight the tile using the hex coordinate. """
        self._tiles[hex]['background'].color = palette['green'][0]

    def highlight(self, screen_x: int, screen_y: int, color: str):
        """ Highlight the tile that contains the given screen-space coordinate.
        """
        for tile in self._tiles.values():
            if (screen_x, screen_y) in tile[0]:
                tile['background'].color = palette[color][3]
                tile['foreground'].color = palette[color][2]
            else:
                tile['background'].color = palette['green'][0]
                tile['foreground'].color = palette['green'][0]

    def move_player(self, direction: str):
        click_sound.play()
        new_tile = self.boundary_check(self.player_pos, direction)
        self.player_pos = new_tile
        self.highlight_tile(self.player_pos)

        next_position = HexOrientation.center(new_tile, self._radius, self._origin)
        self.player.add_next_position((round(next_position[0][0]), round(next_position[1][0])))
        self._player_trail[new_tile] = 0