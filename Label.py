import pygame
import pygame.font

class Label:
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
        self.button.fill(self.fg_color)
        screen.blit(self.button, (self.x, self.y))
        screen.blit(self.text_surface, self.text_rect)
        
