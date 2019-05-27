from Tiles import *
import random
from datetime import *
import time
import random

class Level():
    def __init__(self, start_xs, start_ys, end_xs, end_ys, available_buttons, initial_number_of_minecarts, number_tests, description, button_board, game, cg_funcs):
        self.description = description
        self.initial_number_of_minecarts = initial_number_of_minecarts
        self.number_of_minecarts = self.initial_number_of_minecarts
        self.button_board = button_board
        self.output_queue = [[]]
        self.input_queue = [{}]
        self.start_xs = start_xs
        self.start_ys = start_ys
        self.number_tests = number_tests
        self.current_test = 0
        
        for (button, button_state) in zip(game.radio_buttons[1:], available_buttons):
            button.state = button_state

        index = 0
        for (x, y) in zip(start_xs, start_ys):
            button_board[x][y].tile = Start()
            self.input_queue.append({})
            index += 1

        index = 0
        for (x, y) in zip(end_xs, end_ys):
            button_board[x][y].tile = End(index)
            self.output_queue.append([])
            index += 1

        self.game = game
        temp_funcs = []
        while len(temp_funcs) < self.number_tests:
            random.shuffle(cg_funcs)
            temp_funcs.extend(cg_funcs)

        self.custom_generate_minecarts = temp_funcs
        if len(temp_funcs) > self.number_tests:
            temp_funcs = temp_funcs[:self.number_tests]

        self.minecarts = []

        self.game.level_description.set_text(description)

    def generate_minecart(self):
        if self.number_of_minecarts == 0:
            # Put Error Message Here.
            self.output_queue = []
            self.number_of_minecarts = self.initial_number_of_minecarts
            self.game.set_editting()
        else:
            self.custom_generate_minecarts[self.current_test](self, self.button_board)
            self.current_test += 1

    def send_minecart(self, enterance, minecart, direction, velocity):
        self.number_of_minecarts = self.number_of_minecarts - 1
        minecart.x = self.start_xs[enterance]
        minecart.y = self.start_ys[enterance]
        minecart.velocity = velocity
        minecart.direction = direction
        self.minecarts.append(minecart)

    def queue_minecart(self, enterance, minecart, direction, velocity, seconds):
        print(seconds)
        minecart.x = self.start_xs[enterance]
        minecart.y = self.start_ys[enterance]
        minecart.velocity = 0
        minecart.direction = direction
        self.input_queue[enterance][minecart] = datetime.now() + timedelta(0, seconds)

    def check_queue(self):
        enterance = 0
        for queue in self.input_queue:
            new_queue = queue.copy()
            for key in queue:
                if queue[key] <= datetime.now():
                    # i have no idea why i use two time classes but it works
                    key.departure_time = time.time()
                    self.send_minecart(enterance, key, key.direction, 1)
                    new_queue.pop(key, None)

            self.input_queue[enterance] = new_queue
            enterance = enterance + 1

    def check_output(self, minecart, identification):
        if minecart.id == self.output_queue[identification][0].id:
            self.output_queue[identification].remove(minecart)
            minecart.kill()
            if sum(len(queue) for queue in self.output_queue) == 0 and self.current_test == self.number_tests:
                self.output_queue = [[]]
                self.number_of_minecarts = self.initial_number_of_minecarts
                self.game.clear()
                self.game.start_button.fg_color = (0, 200, 0)
                self.game.start_button.set_text("Start")
                self.game.mode = "editting"
                self.game.reset_board()
                self.game.next_level()
            elif sum(len(queue) for queue in self.output_queue) == 0:
               self.generate_minecart()

        else:
            self.output_queue[identification] = []
            self.number_of_minecarts = self.initial_number_of_minecarts
            self.game.set_editting()

    # Constructing a level is kinda a weird process...
    # The format is in the Level Constructor.
    level_data = [[[0], [13], [19], [13], [True, False, False, False, False, False, False, False], 1, 1, "Simple. Get the minecart to the exit."],
                  [[0], [13], [19], [0], [True, True, False, False, False, False, False, False], 1, 1, "Now there's a turn! Maybe you can use your new tile to help you here."],
                  [[0], [13], [19], [0], [True, False, True, False, False, False, False, False], 1, 1, "This one is the same as the last round."],
                  [[0], [10], [19, 19], [5, 15], [True, True, True, True, False, False, False, False], 2, 1, "Two minecarts will appear. The first should go to the bottom exit and the second one should go to the top exit."],
                  [[0], [10], [19, 19], [5, 15], [True, True, True, True, False, False, False, False], 2, 1, "Two minecarts will appear. The first should go to the top exit and the second one should go to the bottom exit."],
                  [[0], [10], [19], [10], [True, True, True, True, False, False, False, False], 2, 1, "Four minecarts will appear in quick succession. Make them exit in reverse order."],
                  [[0, 0], [5, 15], [19, 19], [5, 15], [True, True, True, True, True, True, True, False], 2, 1, "Here's another challenge. The first enterance will spout a continous stream of minecarts. Once the second enterance releases a minecart (it'll only release one), the stream should switch to the bottom exit. Bring the bottom minecart to the top exit. Timing is key!"],
                  [[0, 0], [5, 15], [19], [10], [True, True, True, True, True, True, True, False], 2, 3, "This one is pretty tough. A set of three or four minecarts will appear in quick succession from the top enterance. Make them exit in reverse order once a minecart appears from the bottom enterance. The minecart from the bottom enterane should exit last. This will be tested three times."],
                  [[0, 0], [5, 15], [19, 19], [5, 15], [True, True, True, True, False, False, False, True], 2, 1, "Remember that level with the stream of minecarts? Do it again without the Rebound block. The first enterance will spout a continous stream of minecarts. Once the second enterance releases a minecart (it'll only release one), the stream should switch to the bottom exit. Bring the bottom minecart to the top exit."],
                  [[0], [10], [19, 19, 19], [5, 10, 15], [True, True, True, True, True, True, True, True], 2, 1, "Here's a tricky one. There are three exits. A stream of minecarts will flow from the enterance. The first should go to the top, the second to the middle, the third to the bottom, the fourth back to the top, etc. Good luck!"],
                  [[0], [10], [19, 19, 19], [5, 10, 15], [True, True, True, True, True, True, True, True], 2, 1, "If you've gotten this far, congratulations. You've beaten the game. I was too lazy to create an end-game screen so I just added another level and put this stuff in the level description. I hope you had fun! Hopefully it entertained you while we were in Beit Sahour."]]

    def cg_func_1(level, button_board):
        minecart = Minecart(button_board, level, 0)
        level.send_minecart(0, minecart, 0, 1)
        level.output_queue[0].append(minecart)

    def cg_func_4(level, button_board):
        minecart1 = Minecart(button_board, level, 0)
        minecart2 = Minecart(button_board, level, 0)
        level.send_minecart(0, minecart1, 0, 1)
        level.queue_minecart(0, minecart2, 0, 1, 0.3)
        level.output_queue[1].append(minecart1)
        level.output_queue[0].append(minecart2)

    def cg_func_5(level, button_board):
        minecart1 = Minecart(button_board, level, 0)
        minecart2 = Minecart(button_board, level, 0)
        level.send_minecart(0, minecart1, 0, 1)
        level.queue_minecart(0, minecart2, 0, 1, 0.3)
        level.output_queue[1].append(minecart2)
        level.output_queue[0].append(minecart1)

    def cg_func_6(level, button_board):
        minecart1 = Minecart(button_board, level, 0)
        minecart2 = Minecart(button_board, level, 0)
        minecart3 = Minecart(button_board, level, 0)
        minecart4 = Minecart(button_board, level, 0)
        level.send_minecart(0, minecart1, 0, 1)
        level.queue_minecart(0, minecart2, 0, 1, 0.3)
        level.queue_minecart(0, minecart3, 0, 1, 0.6)
        level.queue_minecart(0, minecart4, 0, 1, 0.9)
        level.output_queue[0].append(minecart4)
        level.output_queue[0].append(minecart3)
        level.output_queue[0].append(minecart2)
        level.output_queue[0].append(minecart1)

    def cg_func_7_1(level, button_board):
        minecart1 = Minecart(button_board, level, 0)
        minecart2 = Minecart(button_board, level, 0)
        minecart3 = Minecart(button_board, level, 0)
        minecartend = Minecart(button_board, level, 1)
        level.send_minecart(0, minecart1, 0, 1)
        level.queue_minecart(0, minecart2, 0, 1, 0.3)
        level.queue_minecart(0, minecart3, 0, 1, 0.6)
        level.queue_minecart(1, minecartend, 0, 1, 1)
        level.output_queue[0].append(minecart3)
        level.output_queue[0].append(minecart2)
        level.output_queue[0].append(minecart1)
        level.output_queue[0].append(minecartend)

    def cg_func_7_2(level, button_board):
        minecart1 = Minecart(button_board, level, 0)
        minecart2 = Minecart(button_board, level, 0)
        minecart3 = Minecart(button_board, level, 0)
        minecart4 = Minecart(button_board, level, 0)
        minecartend = Minecart(button_board, level, 1)
        level.send_minecart(0, minecart1, 0, 1)
        level.queue_minecart(0, minecart2, 0, 1, 0.3)
        level.queue_minecart(0, minecart3, 0, 1, 0.6)
        level.queue_minecart(0, minecart4, 0, 1, 0.9)
        level.queue_minecart(1, minecartend, 0, 1, 1)
        level.output_queue[0].append(minecart4)
        level.output_queue[0].append(minecart3)
        level.output_queue[0].append(minecart2)
        level.output_queue[0].append(minecart1)
        level.output_queue[0].append(minecartend)

    def cg_func_8(level, button_board):
        minecarts = []
        for i in range(0, 10):
            minecarts.append(Minecart(button_board, level, 0))

        minecart_splitter = Minecart(button_board, level, 1)
        minecart_splitter_time = random.choice([0.45, 0.75, 1.05, 1.35, 1.65, 1.95, 2.25, 2.55])
        index = int(((minecart_splitter_time - 0.45) / 0.3) + 2)

        time = 0.3
        level.send_minecart(0, minecarts[0], 0, 1)
        level.output_queue[0].append(minecarts[0])
        
        for minecart in minecarts[1:index]:
            level.queue_minecart(0, minecart, 0, 1, time)
            level.output_queue[0].append(minecart)
            time += 0.3
        for minecart in minecarts[index:]:
            level.queue_minecart(1, minecart, 0, 1, time)
            level.output_queue[1].append(minecart)
            time += 0.3
            
        level.queue_minecart(0,  minecart_splitter, 0, 1, minecart_splitter_time)
        level.output_queue[0].append(minecarts[0])

    def cg_func_9(level, button_board):
        minecarts = []
        for i in range(0, 10):
            minecarts.append(Minecart(button_board, level, 0))

        minecart_splitter = Minecart(button_board, level, 1)
        minecart_splitter_time = random.choice([2.25, 3.15, 4.05, 4.95, 5.85, 6.75])
        index = int(((minecart_splitter_time - 1.35) / 0.9) + 2)
        print("mc" + str(minecart_splitter_time))
        time = 0.9
        level.send_minecart(0, minecarts[0], 0, 1)
        level.output_queue[0].append(minecarts[0])
        
        for minecart in minecarts[1:index]:
            level.queue_minecart(0, minecart, 0, 1, time)
            level.output_queue[0].append(minecart)
            time += 0.9
        for minecart in minecarts[index:]:
            level.queue_minecart(1, minecart, 0, 1, time)
            level.output_queue[1].append(minecart)
            time += 0.9
            
        level.queue_minecart(0,  minecart_splitter, 0, 1, minecart_splitter_time)
        level.output_queue[0].append(minecarts[0])
        
    def cg_func_10(level, button_board):
        minecarts = []
        minecart = Minecart(button_board, level, 0)
        level.send_minecart(0, minecart, 0, 1)
        level.output_queue[0].append(minecart)
        
        for i in range(1, 10):
            minecart = Minecart(button_board, level, 0)
            level.queue_minecart(0, minecart, 0, 1, i * 0.3)
            level.output_queue[i % 3].append(minecart)
        
    level_custom_generation_funcs = [[cg_func_1], [cg_func_1], [cg_func_1], [cg_func_4], [cg_func_5], [cg_func_6], [cg_func_8], [cg_func_7_1, cg_func_7_2], [cg_func_9], [cg_func_10], [cg_func_10]]
    
    def get_level(level_number, button_board, game):
        return Level(*Level.level_data[level_number], button_board, game, Level.level_custom_generation_funcs[level_number])
