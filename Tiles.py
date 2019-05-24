from Minecart import *
import math

class Tile():
    def __init__(self, fg_color):
        self.fg_color = fg_color
        
    def do_action(self, minecart):
        minecart.kill()

    def construct_tile(name):
        return tile_directory[name]()

class Empty(Tile):
    def __init__(self):
        Tile.__init__(self, (255, 255, 255))
        
    def do_action(self, minecart):
        minecart.kill()
        minecart.level.game.set_editting()

class Straight(Tile):
    def __init__(self):
        Tile.__init__(self, (175, 245, 245))
        
    def do_action(self, minecart):
        pass

class Left(Tile):
    def __init__(self):
        Tile.__init__(self, (245, 245, 175))
        
    def do_action(self, minecart):
        minecart.direction -= (math.pi/2) % (2 * math.pi)

class Right(Tile):
    def __init__(self):
        Tile.__init__(self, (245, 175, 245))
        
    def do_action(self, minecart):
        minecart.direction += (math.pi/2) % (2 * math.pi)

class Start(Tile):
    def __init__(self):
        Tile.__init__(self, (0, 200, 0))

    def do_action(self, minecart):
        pass

class End(Tile):
    def __init__(self, identification):
        self.identification = identification
        Tile.__init__(self, (200, 0, 0))

    def do_action(self, minecart):
        minecart.level.check_output(minecart, self.identification)

class Switch(Tile):
    def __init__(self):
        Tile.__init__(self, (145, 75, 145))
        self.is_right = True
    
    def do_action(self, minecart):
        if self.is_right:
            minecart.direction += (math.pi/2)
            self.fg_color = (145, 145, 75)
        else:
            minecart.direction -= (math.pi/2)
            self.fg_color = (145, 75, 145)

        minecart.direction %= (2 * math.pi)
        
        self.is_right = not self.is_right

    def reset(self):    
        self.fg_color = (145, 75, 145)
        self.is_right = True

class Bounce(Tile):
    def __init__(self):
        Tile.__init__(self, (255, 200, 75))

    def do_action(self, minecart):
        minecart.direction += pi
        minecart.direction %= (2 * math.pi)

tile_directory = {"Erase":    Empty,
                  "Straight": Straight,
                  "Left":     Left,
                  "Right":    Right,
                  "Switch":   Switch,
                  "Bounce":   Bounce}

