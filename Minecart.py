from math import *
from pygame import *
import time
import itertools
import string
from random import choices

class Minecart:
    def __init__(self, board, level, enterance):
        self.x = level.start_xs[enterance] * 25 + 105 
        self.y = level.start_ys[enterance] * 25 + 5
        self.direction = 0
        self.color = (200, 200, 200)
        self.surface = Surface((15, 15))
        self.button_board = board
        self.alive = True
        self.level = level
        self.id = list(itertools.islice(Minecart.gen_id(), 1))[0]
        self.moving = True
        
        self.departure_time = time.time()
        self.set_destination()
        self.time_speed = 0.15

    def set_destination(self):
        if not self.moving:
            return
        self.old_x = self.x
        self.old_y = self.y
        self.destination_x = self.x + 25 * cos(self.direction)
        self.destination_y = self.y + 25 * sin(self.direction)
        self.departure_time = time.time()

    def update(self):
        if self.level.game.mode == "editting":
            return

        elapsed_time = time.time() - self.departure_time
        self.x = self.old_x + (elapsed_time / self.time_speed) * (self.destination_x - self.old_x)
        self.y = self.old_y + (elapsed_time / self.time_speed) * (self.destination_y - self.old_y)

        if elapsed_time > self.time_speed:
            self.x = self.destination_x
            self.y = self.destination_y
            try:
                self.button_board[int(round((self.x - 105) / 25))][int(round((self.y - 5) / 25))].tile.do_action(self)
            except IndexError as e:
                self.kill()
            self.set_destination()
        
    def draw(self, screen):
        if self.alive:
            self.surface.fill(self.color)
            screen.blit(self.surface, (self.x, self.y))

    def kill(self):
        if self.alive:
            self.alive = False      
            self.level.minecarts.remove(self)

    def gen_id():
        history = []
        charset = string.ascii_lowercase + string.digits
        while True:
            new_id = "".join(choices(charset, k=8))
            if new_id not in history:
                history.append(new_id)
                yield new_id
