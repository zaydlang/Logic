from Tiles import *
import random
from datetime import *
import time

class Level():
    def __init__(self, start_x, start_y, end_xs, end_ys, available_buttons, initial_number_of_minecarts, description, button_board, game, cg_func):
        self.start_x = start_x * 25 + 105
        self.start_y = start_y * 25 + 5
        self.description = description
        self.initial_number_of_minecarts = initial_number_of_minecarts
        self.number_of_minecarts = self.initial_number_of_minecarts
        self.button_board = button_board
        self.output_queue = [[]]

        for (button, button_state) in zip(game.radio_buttons[1:], available_buttons):
            button.state = button_state

        button_board[int((self.start_x - 105) / 25)][int((self.start_y - 5) / 25)].tile = Start()
        index = 0
        for (x, y) in zip(end_xs, end_ys):
            button_board[x][y].tile = End(index)
            self.output_queue.append([])
            index += 1

        self.game = game
        self.custom_generate_minecart = cg_func

        self.input_queue = {}
        self.minecarts = []

        self.game.level_description.set_text(description)

    def generate_minecart(self):
        if self.number_of_minecarts == 0:
            # Put Error Message Here.
            self.output_queue = []
            self.number_of_minecarts = self.initial_number_of_minecarts
            self.game.set_editting()
        else:
            self.custom_generate_minecart(self, self.button_board)

    def send_minecart(self, minecart, direction, velocity):
        self.number_of_minecarts = self.number_of_minecarts - 1
        minecart.x = self.start_x
        minecart.y = self.start_y
        minecart.velocity = velocity
        minecart.direction = direction
        self.minecarts.append(minecart)

    def queue_minecart(self, minecart, direction, velocity, seconds):
        minecart.x = self.start_x
        minecart.y = self.start_y
        minecart.velocity = 0
        minecart.direction = direction
        self.input_queue[minecart] = datetime.now() + timedelta(0, seconds)

    def check_queue(self):
        new_queue = self.input_queue.copy()
        for key in self.input_queue:
            if self.input_queue[key] <= datetime.now():
                # i have no idea why i use two time classes but it works
                key.departure_time = time.time()
                self.send_minecart(key, key.direction, 1)
                new_queue.pop(key, None)

        self.input_queue = new_queue

    def check_output(self, minecart, identification):
        print("uwu" + str(identification))
        if minecart.id == self.output_queue[identification][0].id:
            self.output_queue[identification].remove(minecart)
            minecart.kill()
            if self.number_of_minecarts == 0 and sum(len(queue) for queue in self.output_queue) == 0:
                self.output_queue = [[]]
                self.number_of_minecarts = self.initial_number_of_minecarts
                self.game.clear()
                self.game.set_editting()
                self.game.next_level()

        else:
            self.output_queue[identification] = []
            self.number_of_minecarts = self.initial_number_of_minecarts
            self.game.set_editting()

    # Constructing a level is kinda a weird process...
    # The format is in the Level Constructor.
    level_data = [[0, 13, [19], [13], [True, False, False, False, False, False, False, False], 1, "Simple. Get the minecart to the exit."],
                  [0, 13, [19], [0], [True, True, False, False, False, False, False, False], 1, "Now there's a turn! Maybe you can use your new tile to help you here."],
                  [0, 13, [19], [0], [True, False, True, False, False, False, False, False], 1, "This one is the same as the last round."],
                  [0, 10, [19, 19], [5, 15], [True, True, True, True, False, False, False, False], 2, "Two minecarts will appear. The first should go to the bottom exit and the second one should go to the top exit."],
                  [0, 10, [19, 19], [5, 15], [True, True, True, True, False, False, False, False], 2, "Two minecarts will appear. The first should go to the top exit and the second one should go to the bottom exit."]]

    def cg_func_1(level, button_board):
        minecart = Minecart(button_board, level)
        level.send_minecart(minecart, 0, 1)
        level.output_queue[0].append(minecart)

    def cg_func_4(level, button_board):
        minecart1 = Minecart(button_board, level)
        minecart2 = Minecart(button_board, level)
        level.send_minecart(minecart1, 0, 1)
        level.queue_minecart(minecart2, 0, 1, 0.3)
        level.output_queue[1].append(minecart1)
        level.output_queue[0].append(minecart2)

    def cg_func_5(level, button_board):
        minecart1 = Minecart(button_board, level)
        minecart2 = Minecart(button_board, level)
        level.send_minecart(minecart1, 0, 1)
        level.queue_minecart(minecart2, 0, 1, 0.3)
        level.output_queue[1].append(minecart2)
        level.output_queue[0].append(minecart1)
        
    level_custom_generation_funcs = [cg_func_1, cg_func_1, cg_func_1, cg_func_4, cg_func_5]
    
    def get_level(level_number, button_board, game):
        return Level(*Level.level_data[level_number], button_board, game, Level.level_custom_generation_funcs[level_number])
