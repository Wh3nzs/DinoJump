import random
import pygame

from settings import HEIGHT, WIDTH, screen

class birds:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 30
        self.height = 30

        self.gravity = 0
        self.velocity = [0,0]

        self.image = pygame.image.load("assets/bird.png").convert_alpha()

    def update(self, dt):

        self.pos = (self.x, self.y)
        self.x += self.velocity[0] * dt

        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity[1] = 0
        else:
            self.y += self.velocity[1]
            self.velocity[1] += self.gravity * dt

        if self.y < 0:
            self.y = self.height
            self.y = 0
            self.velocity[1] = 0

        if(self.x < -self.width):
            self.spawn()
            self.delete()


    def draw(self):
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        pygame.draw.rect(screen, (0,0,255), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 1) # Hitbox
        rect = scaled_image.get_rect(center=(self.x, self.y))
        screen.blit(scaled_image, rect)

    def spawn(self):
        self.x = WIDTH + self.width + random.randint(0, 700)
        self.y = random.randint(300, HEIGHT - 75)
        self.velocity[0] = -200  # Move left at 200 pixels per second

    def collision(self, dino):
        bird_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return bird_rect.colliderect(dino.rect)
    def delete(self): 
        return 1 
        del self

class cati:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 30
        self.height = 30

        self.gravity = 0
        self.velocity = [0,0]

        self.image = pygame.image.load("assets/cati.png").convert_alpha()

    def update(self, dt):

        self.pos = (self.x, self.y)
        self.x += self.velocity[0] * dt

        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity[1] = 0
        else:
            self.y += self.velocity[1]
            self.velocity[1] += self.gravity * dt

        if self.y < 0:
            self.y = self.height
            self.y = 0
            self.velocity[1] = 0

        if(self.x < -self.width):
            self.spawn()
            self.delete()
    def colision(self, dino):
        cati_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return cati_rect.colliderect(dino.rect)

    def draw(self):
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        pygame.draw.rect(screen, (255,0,255), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 1) # Hitbox
        rect = scaled_image.get_rect(center=(self.x, self.y))
        screen.blit(scaled_image, rect)

    def spawn(self):
        self.x = WIDTH + self.width + random.randint(0, 1000)
        self.y = HEIGHT - self.height / 2
        self.velocity[0] = -200  # Move left at 200 pixels per second

    def collision(self, dino):
        cati_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return cati_rect.colliderect(dino.rect)
    def delete(self):
        return 1 
        del self
    
birds = [birds(WIDTH + i * 300, random.randint(50, HEIGHT - 50)) for i in range(5)]
catis = [cati(WIDTH + i * 300, HEIGHT - 15) for i in range(3)]
