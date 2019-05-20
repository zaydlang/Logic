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
        self.button_font = pygame.font.Font("Code New Roman.otf", 20)
        self.create_widgets()
        self.create_board()
        self.level = Level(105, 55, 550, 105, "Test", self.button_board, self)
        self.minecart = None
        self.mode = "editting"

    def create_board(self):
        self.button_board = [[TileButton(x * 25 + 100, y * 25, 25, 25, "", self.button_font, (0, 0, 0), (255, 255, 255), Empty()) for y in range(20)] for x in range(20)]
        
    def create_widgets(self):
        self.radio_buttons.append(RadioButton(0, 0, 100, 50, "Straight", self.button_font, (0, 0, 0), (175, 245, 245)))
        self.radio_buttons.append(RadioButton(0, 50, 100, 50, "Left", self.button_font, (0, 0, 0), (245, 245, 175)))
        self.radio_buttons.append(RadioButton(0, 100, 100, 50, "Right", self.button_font, (0, 0, 0), (245, 175, 245)))
        self.radio_buttons.append(RadioButton(0, 450, 100, 50, "Erase", self.button_font, (0, 0, 0), (150, 150, 150)))

        self.start_button = Button(600, 350, 100, 50, "Start", self.button_font, (255, 255, 255), (0, 200, 0))
        self.clear_button = Button(600, 450, 100, 50, "Clear", self.button_font, (255, 255, 255), (255, 0, 0))
        self.level_text = Label(600, 0, 100, 50, "Level 1", self.button_font, (0, 0, 0), (175, 175, 175))
    def dispatch(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if pygame.mouse.get_pressed()[0]:
            if self.mode == "editting":
                for button in self.radio_buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.set_pressed()

                for buttons in self.button_board:
                    for button in buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()) and self.radio_buttons[0].button_pressed is not None:
                            button.tile = Tile.construct_tile(self.radio_buttons[0].button_pressed.text)
                            
                if self.clear_button.rect.collidepoint(pygame.mouse.get_pos()):
                    for buttons in self.button_board:
                        for button in buttons:
                            button.tile = Empty()

            if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                if self.mode == "editting":
                    self.set_testing()
                elif self.mode == "testing":
                    self.set_editting()

    def set_testing(self):
        self.minecart = Minecart(self.button_board, self.level)
        self.mode = "testing"
        self.start_button.fg_color = (200, 200, 0)
        self.start_button.set_text("Stop")

    def set_editting(self):
        print("cmon")
        self.start_button.fg_color = (0, 200, 0)
        self.start_button.set_text("Start")
        self.minecart = None
        self.mode = "editting"

    def run(self):
        while True:
            for e in pygame.event.get():
                self.dispatch(e)
        
            pygame.display.flip()
                
            for buttons in self.button_board:
                for button in buttons:
                    button.draw(screen)
                
            for button in self.radio_buttons:
                button.draw(screen)

            if self.mode == "testing":
                self.minecart.draw(screen)
                self.minecart.update()
                # Update may chanage the value of mode, so it must go after draw.

            self.clear_button.draw(screen)
            self.start_button.draw(screen)
            self.level_text.draw(screen)
                
pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Logic")
root = Application()
root.run()
