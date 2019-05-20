from Tiles import *
import random

class Level():
    def __init__(self, start_x, start_y, end_x, end_y, description, button_board, game):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.description = description
        self.initial_number_of_minecarts = 3
        self.number_of_minecarts = 3

        button_board[int((self.start_x - 105) / 25)][int((self.start_y - 5) / 25)].tile = Start()
        button_board[int((self.end_x - 105) / 25)][int((self.end_y - 5) / 25)].tile = End()

        self.output_queue = []
        self.game = game

    def generate_minecart(self, minecart):
        self.number_of_minecarts = self.number_of_minecarts - 1
        minecart.x = self.start_x
        minecart.y = self.start_y
        minecart.velocity = 1
        minecart.direction = random.choice([0])
        self.output_queue.append(minecart)

    def check_output(self, minecart):
        if minecart.id == self.output_queue[0].id:
            self.output_queue.remove(minecart)
            if self.number_of_minecarts == 0:
                self.output_queue = []
                self.number_of_minecarts = self.initial_number_of_minecarts
                self.game.set_editting()
            self.game.minecart = Minecart(minecart.button_board, minecart.level)

        else:
            self.output_queue = []
            self.number_of_minecarts = self.initial_number_of_minecarts
            self.game.set_editting()
        
        
