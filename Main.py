import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dino jump")
pygame.display.set_icon(pygame.image.load("assets/dino.png"))

class Dino:
    def __init__(self):
        self.image = pygame.image.load("assets/dino.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, HEIGHT - 100)
        self.velocity = 0
        self.gravity_force = 981  # Pixels per second squared
    def gravity(self, dt):
        self.velocity += self.gravity_force * dt
        self.rect.y += self.velocity * dt
        self.rect.y = round(self.rect.y)

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self,dt):
        self.velocity = -350  # Jump velocity in pixels per second

    def groundCheck(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            return True
        return False
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)



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

    def draw(self):
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        # pygame.draw.rect(screen, (0,0,255), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 1) # Hitbox
        rect = scaled_image.get_rect(center=(self.x, self.y))
        screen.blit(scaled_image, rect)

    def spawn(self):
        self.x = WIDTH + self.width + random.randint(0, 700)
        self.y = random.randint(0, HEIGHT - self.height)
        self.velocity[0] = -200  # Move left at 200 pixels per second

    def collision(self, dino):
        bird_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return bird_rect.colliderect(dino.rect)

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

    def draw(self):
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        # pygame.draw.rect(screen, (255,0,255), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 1) # Hitbox
        rect = scaled_image.get_rect(center=(self.x, self.y))
        screen.blit(scaled_image, rect)

    def spawn(self):
        self.x = WIDTH + self.width + random.randint(0, 700)
        self.y = HEIGHT - self.height / 2
        self.velocity[0] = -200  # Move left at 200 pixels per second

    def collision(self, dino):
        cati_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return cati_rect.colliderect(dino.rect)

dino = Dino()
birds = [birds(WIDTH + i * 300, random.randint(50, HEIGHT - 50)) for i in range(5)]
catis = [cati(WIDTH + i * 300, HEIGHT - 15) for i in range(3)]
def GameLoop():
    running = True
    while running:

        dt = pygame.time.Clock().tick(60) / 1000  # Delta time in seconds

        screen.fill((25, 25, 25))
        dino.draw(screen) 
        dino.gravity(dt)  # Assuming a frame rate of 60 FPS

        # put all draws before the flip
        for bird in birds:
            bird.velocity[0] = -500  # Move left at 500 pixels per second
            bird.update(dt)
            bird.draw()
        for cati in catis:
            cati.velocity[0] = -500  # Move left at 500 pixels per
            cati.update(dt)
            cati.draw()

            if bird.collision(dino):
                print("Collision detected!")


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    if dino.groundCheck():
                        dino.jump(dt)
def diedscreen():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
def menu():
    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

GameLoop()