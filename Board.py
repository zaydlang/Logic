from Tiles import *

class Board():
    def __init__(width, height, layout):
        self.layout = [[Tile for x in range(width)] for y in range(height)]

    def set(column, row, tile):
        self.layout[column][row] = tile
