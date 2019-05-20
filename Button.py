import pygame
import pygame.font

class Button:
    def __init__(self, x, y, width, height, text, font, text_color, fg_color):
        self.button = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.hovered = False
        self.rect = self.button.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.fg_color = fg_color
        self.hover_color = tuple(max(0, x - 50) for x in list(fg_color))
        self.font = font
        self.text_color = text_color

    def set_text(self, text):
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        self.check_hovered()
        self.button.fill(self.get_color())
        screen.blit(self.button, (self.x, self.y))
        screen.blit(self.text_surface, self.text_rect)

    def check_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
        
    def get_color(self):
        if self.hovered:
            return self.hover_color
        else:
            return self.fg_color

class TileButton(Button):
    def __init__(self, x, y, width, height, text, font, text_color, fg_color, tile):
        Button.__init__(self, x, y, width, height, text, font, text_color, fg_color)
        self.tile = tile

    def get_color(self):
        if self.hovered:
            return tuple(max(0, x - 50) for x in list(self.tile.fg_color))
        else:
            return self.tile.fg_color

class RadioButton(Button):
    button_pressed = None

    def __init__(self, x, y, width, height, text, font, text_color, fg_color):
        Button.__init__(self, x, y, width, height, text, font, text_color, fg_color)
        self.buttons = []

    def get_pressed(self):
        return RadioButton.button_pressed

    def set_pressed(self):
        RadioButton.button_pressed = self

    def get_color(self):
        if self.hovered or self is RadioButton.button_pressed:
            return self.hover_color
        else:
            return self.fg_color

        
