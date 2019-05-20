from Minecart import *
import math

class Tile():
    def do_action(self, minecart):
        minecart.kill()
    
    def __init__(self, fg_color):
        self.fg_color = fg_color

    def construct_tile(name):
        return tile_directory[name]

class Empty(Tile):
    def do_action(self, minecart):
        minecart.kill()
        minecart.level.game.set_editting()

    def __init__(self):
        Tile.__init__(self, (255, 255, 255))

class Straight(Tile):
    def do_action(self, minecart):
        pass
    
    def __init__(self):
        Tile.__init__(self, (175, 245, 245))

class Left(Tile):
    def do_action(self, minecart):
        minecart.direction -= (math.pi/2) % (2 * math.pi)
    
    def __init__(self):
        Tile.__init__(self, (245, 245, 175))

class Right(Tile):
    def do_action(self, minecart):
        minecart.direction += (math.pi/2) % (2 * math.pi)
    
    def __init__(self):
        Tile.__init__(self, (245, 175, 245))

class Start(Tile):
    def do_action(self, minecart):
        pass

    def __init__(self):
        Tile.__init__(self, (0, 200, 0))

class End(Tile):
    def do_action(self, minecart):
        minecart.level.check_output(minecart)

    def __init__(self):
        Tile.__init__(self, (200, 0, 0))

tile_directory = {"Erase":    Empty(),
                  "Straight": Straight(),
                  "Left":     Left(),
                  "Right":    Right()}

