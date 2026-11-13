import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dino jump")
pygame.display.set_icon(pygame.image.load("assets/dino.png"))

score_font = pygame.font.SysFont("fixed", 30)


font = pygame.font.Font(None, 36)
