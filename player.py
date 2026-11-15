import pygame

from settings import HEIGHT, screen
from save_data import active_player
from skins import SKINS

class Dino:
    def __init__(self): 
        skin = SKINS.get(active_player()["skin"], SKINS["default"])
        sprite = pygame.image.load(skin[1]).convert_alpha()
        crouch = pygame.image.load("assets/squat.png").convert_alpha() if skin == SKINS["default"] else sprite
        self.image = pygame.transform.scale(sprite, (50, 50))
        self.standing_image = pygame.transform.scale(sprite, (30, 50))
        self.squatimg = pygame.transform.scale(crouch, (50, 30))

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, HEIGHT - 100)
        self.velocity = 0
        self.gravity_force = 1200  # Pixels per second squared
        self.mode = None
    def gravity(self, dt):
        self.velocity += self.gravity_force * dt
        self.rect.y += self.velocity * dt
        self.rect.y = round(self.rect.y)

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self,dt):
        self.velocity = -350  # Jump velocity in pixels per second
    def inputhanderler(self, event):
        crouching = pygame.key.get_pressed()[pygame.K_s]
        self.mode = "normal"
        self.image = self.squatimg if crouching else self.standing_image
        self.gravity_force = 2000 if crouching else 850
        if self.rect.size != self.image.get_size():
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.groundCheck():
                self.velocity = -350

    def update(self):
        # Update the rect position based on the current image size
        midbottom = self.rect.midbottom
        self.rect = self.image.get_rect(midbottom=midbottom)

    def groundCheck(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            return True
        return False
        

    def draw(self, surface):
        from gameplay import dino

        surface.blit(self.image, self.rect)

        pygame.draw.rect(screen, (255, 0, 0), dino.rect, 2)



