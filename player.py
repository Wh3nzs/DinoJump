import pygame

from settings import HEIGHT, screen

class Dino:
    def __init__(self): 
        self.image = pygame.image.load("assets/dino.png").convert_alpha()
        self.squatimg = pygame.image.load("assets/squat.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.squatimg = pygame.transform.scale(self.squatimg, (50, 30))

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
        keys = pygame.key.get_pressed()

        self.original_image = self.image          # keep the untouched sprite
        self.mode = "normal"

        # in update / handle_input
        keys = pygame.key.get_pressed()

        crouching = keys[pygame.K_s]
        size = (50, 30) if crouching else (30, 50)
        self.image = self.squatimg if crouching else self.original_image
        self.gravity_force = 2000 if crouching else 850
        self.original_image = pygame.image.load("assets/dino.png").convert_alpha() if not crouching else pygame.image.load("assets/squat.png").convert_alpha()

        if self.rect.size != size:                # only rebuild when the state changes
            midbottom = self.rect.midbottom       # remember where the feet are
            self.image = pygame.transform.scale(self.original_image, size)
            self.rect = self.image.get_rect(midbottom=midbottom)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.groundCheck():
                self.velocity = -350
            if event.key == pygame.K_p:           # toggle instead of blocking on input()
                size = (2, 2)

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



