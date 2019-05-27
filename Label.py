import pygame
import pygame.font
import textwrap

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
        self.font = font
        self.text_color = text_color
        self.set_text(text)
        self.fg_color = fg_color
        self.hover_color = tuple(max(0, x - 50) for x in list(fg_color))

    def set_text(self, text):
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.text = text

    # Thanks https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    def blit_text(self, surface):
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = self.x, self.y
        self.old_x = x
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, self.text_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = self.old_x  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = self.old_x  # Reset the x.
            y += word_height  # Start on new row.

    def draw(self, screen):
        self.button.fill(self.fg_color)
        screen.blit(self.button, (self.x, self.y))
        self.blit_text(screen)
        
