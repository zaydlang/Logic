import pygame
import pygame.font
from Tiles import *
from Board import *
from Button import *
from Minecart import *
from Level import *
from Label import *

class Application:
    def __init__(self):
        self.radio_buttons = []
        self.level_number = 10
        
        self.button_font = pygame.font.Font("Code New Roman.otf", 20)
        self.create_widgets()
        self.create_board()
        self.level = Level.get_level(self.level_number, self.button_board, self)
        self.mode = "editting"
        
    def create_board(self):
        self.button_board = [[TileButton(x * 25 + 100, y * 25, 25, 25, "", self.button_font, (0, 0, 0), (255, 255, 255), Empty()) for y in range(20)] for x in range(20)]
        
    def create_widgets(self):
        self.radio_buttons.append(RadioButton(0, 450, 100, 50, "Erase", self.button_font, (0, 0, 0), (150, 150, 150)))

        self.radio_buttons.append(RadioButton(0, 0, 100, 50, "Straight", self.button_font, (0, 0, 0), (175, 245, 245)))
        self.radio_buttons.append(RadioButton(0, 50, 100, 50, "Left", self.button_font, (0, 0, 0), (245, 245, 175)))
        self.radio_buttons.append(RadioButton(0, 100, 100, 50, "Right", self.button_font, (0, 0, 0), (245, 175, 245)))
        self.radio_buttons.append(RadioButton(0, 150, 100, 50, "Switch", self.button_font, (0, 0, 0), (145, 75, 145)))
        self.radio_buttons.append(RadioButton(0, 200, 100, 50, "Trigger", self.button_font, (0, 0, 0), (150, 125, 125)))
        self.radio_buttons.append(RadioButton(0, 250, 100, 50, "Wait", self.button_font, (0, 0, 0), (250, 225, 225)))
        self.radio_buttons.append(RadioButton(0, 300, 100, 50, "Rebound", self.button_font, (0, 0, 0), (245, 175, 175)))
        self.radio_buttons.append(RadioButton(0, 350, 100, 50, "Bounce", self.button_font, (0, 0, 0), (255, 200, 75)))

        self.start_button = Button(600, 350, 100, 50, "Start", self.button_font, (255, 255, 255), (0, 200, 0))
        self.clear_button = Button(600, 450, 100, 50, "Clear", self.button_font, (255, 255, 255), (255, 0, 0))
        self.level_text = Label(600, 0, 100, 50, "Level " + str(self.level_number + 1), self.button_font, (0, 0, 0), (175, 175, 175))

        self.level_description_label = Label(0, 500, 150, 50, "Description:", self.button_font, (0, 0, 0), (235, 235, 235))
        self.level_description = Label(0, 550, 700, 150, "you are not supposed to see this text restart the game", self.button_font, (0, 0, 0), (235, 235, 235))

    def next_level(self):
        self.level_number = self.level_number + 1
        self.level = Level.get_level(self.level_number, self.button_board, self)
        self.level_text.set_text("Level " + str(self.level_number + 1))
        
    def clear(self):
        for buttons in self.button_board:
            for button in buttons:
                button.tile = Empty()

    def reset_board(self):
        for buttons in self.button_board:
            for button in buttons:
                if isinstance(button.tile, Switch):
                    button.tile.reset()
                if isinstance(button.tile, Wait):
                    button.tile = Wait()
                if isinstance(button.tile, Rebound):
                    button.tile = Rebound()
                
    def dispatch(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if pygame.mouse.get_pressed()[0]:
            if self.mode == "editting":
                for button in self.radio_buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()) and button.state:
                        button.set_pressed()

                for buttons in self.button_board:
                    for button in buttons:
                        if not isinstance(button.tile, Start) and not isinstance(button.tile, End):
                            if button.rect.collidepoint(pygame.mouse.get_pos()) and self.radio_buttons[0].button_pressed is not None:
                                button.tile = Tile.construct_tile(self.radio_buttons[0].button_pressed.text)
                            
                if self.clear_button.rect.collidepoint(pygame.mouse.get_pos()):
                    for buttons in self.button_board:
                        for button in buttons:
                            if not isinstance(button.tile, Start) and not isinstance(button.tile, End):
                                button.tile = Empty()

            if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                if self.mode == "editting":
                    self.set_testing()
                elif self.mode == "testing":
                    self.set_editting()

    def set_testing(self):
        self.level.generate_minecart()
        self.mode = "testing"
        self.start_button.fg_color = (200, 200, 0)
        self.start_button.set_text("Stop")

    def set_editting(self):
        self.start_button.fg_color = (0, 200, 0)
        self.start_button.set_text("Start")
        self.mode = "editting"

        self.level = Level.get_level(self.level_number, self.button_board, self)

        self.reset_board()

    def run(self):
        while True:
            screen.fill((0, 0, 0))
            
            for e in pygame.event.get():
                self.dispatch(e)
                
            for buttons in self.button_board:
                for button in buttons:
                    button.draw(screen)
                
            for button in self.radio_buttons:
                button.draw(screen)

            if self.mode == "testing":
                for minecart in self.level.minecarts:
                    minecart.draw(screen)
                    minecart.update()
                    self.level.check_queue()
                # Update may chanage the value of mode, so it must go after draw.

            self.clear_button.draw(screen)
            self.start_button.draw(screen)
            self.level_text.draw(screen)
            pygame.draw.rect(screen, (235, 235, 235), (0, 500, 700, 200))
            self.level_description_label.draw(screen)
            self.level_description.draw(screen)
            
            pygame.display.flip()
                
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Logic")
root = Application()
root.run()
