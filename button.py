import pygame

class Button:
    def __init__(self, text, x, y, width, height, callback, font, color=(255, 255, 255), bg=(50, 50, 50)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = font.render(text, True, color)
        self.callback = callback
        self.font = font
        self.color = color
        self.bg = bg
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg, self.rect)
        screen.blit(self.text, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()
