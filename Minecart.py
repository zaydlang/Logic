from math import *
from pygame import *

class Minecart:
    def __init__(self, board, level):
        level.generate_minecart(self)
        self.color = (200, 200, 200)
        self.surface = Surface((15, 15))
        self.button_board = board
        self.alive = True
        self.level = level
        self.id = self.gen_id()

    def update(self):
        i = (self.x - 105) / 25
        j = (self.y - 5) / 25

        if i.is_integer() and j.is_integer():
            try:
                current_tile = self.button_board[int(i)][int(j)].tile
                current_tile.do_action(self)
            except Exception as e:
                print(e)
                self.alive = False

        self.x = self.x + self.velocity * cos(self.direction)
        self.y = self.y + self.velocity * sin(self.direction)
        
    def draw(self, screen):
        if self.alive:
            self.surface.fill(self.color)
            screen.blit(self.surface, (self.x, self.y))

    def kill(self):
        self.alive = False

    def gen_id(self):
        history = []
        charset = string.ascii_lowercase + string.digits
        while True:
            new_id = "".join(choices(charset, k=8))
            if new_id not in history:
                history.append(new_id)
                yield new_id
