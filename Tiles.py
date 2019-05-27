from Minecart import *
import math

class Tile():
    def __init__(self, fg_color):
        self.fg_color = fg_color
        
    def do_action(self, minecart):
        minecart.kill()

    def construct_tile(name):
        return tile_directory[name]()

    def release(self):
        pass

    def toggle(self):
        pass

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

class Trigger(Tile):
    def __init__(self):
        Tile.__init__(self, (150, 125, 125))

    def do_action(self, minecart):
        board = minecart.level.button_board
        i = 0
        j = 0
        
        for buttons in board:
            j = 0
            for button in buttons:
                if button.tile == self:
                    try:
                        board[i + 1][j].tile.release()
                        board[i + 1][j].tile.toggle()
                    except IndexError as e:
                        pass
                    try:
                        board[i][j + 1].tile.release()
                        board[i][j + 1].tile.toggle()
                    except IndexError as e:
                        pass
                    try:
                        board[i - 1][j].tile.release()
                        board[i - 1][j].tile.toggle()
                    except IndexError as e:
                        pass
                    try:
                        board[i][j - 1].tile.release()
                        board[i][j - 1].tile.toggle()
                    except IndexError as e:
                        pass
                    return
                j += 1
            i += 1
            
class Wait(Tile):
    def __init__(self):
        Tile.__init__(self, (250, 225, 225))
        self.old_direction = 0
        self.minecart = None
        self.disabled = False
        
    def do_action(self, minecart):
        if not self.disabled:
            if not self.minecart == None and not self.minecart.id == minecart.id:
                minecart.kill()
                minecart.level.game.set_editting()

            self.minecart = minecart
            minecart.moving = False
            self.old_direction = minecart.direction
        else:
            self.disabled = False

    def release(self):
        if not self.minecart == None:
            self.minecart.direction = self.old_direction
            self.minecart.moving = True
            self.minecart = None
            self.disabled = True

class Rebound(Tile):
    def __init__(self):
        Tile.__init__(self, (125, 195, 195))
        self.is_bounce = False

    def do_action(self, minecart):
        if self.is_bounce:
            minecart.direction += pi
            minecart.direction %= (2 * math.pi)
            
    def toggle(self):
        print("owo")
        self.is_bounce = not self.is_bounce

        if self.is_bounce:
            self.fg_color = (155, 100, 25)
        else:
            self.fg_color = (125, 195, 195)
        
tile_directory = {"Erase":    Empty,
                  "Straight": Straight,
                  "Left":     Left,
                  "Right":    Right,
                  "Switch":   Switch,
                  "Bounce":   Bounce,
                  "Trigger":  Trigger,
                  "Wait":     Wait,
                  "Rebound":  Rebound}

