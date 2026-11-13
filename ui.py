import pygame

from settings import HEIGHT, WIDTH

class button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
buttons = [button(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50, "Start Game"),
           button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Shop")]

death_buttons = [
    button(WIDTH // 2 - 100, HEIGHT - 150, 200, 50, "Start Game"),
    button(WIDTH // 2 - 100, HEIGHT - 85, 200, 50, "Shop"),
]

