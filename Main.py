import pygame, random, json, os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dino jump")
pygame.display.set_icon(pygame.image.load("assets/dino.png"))


font = pygame.font.Font(None, 36)
class Dino:
    def __init__(self):
        self.image = pygame.image.load("assets/dino.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

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

        if keys[pygame.K_s]:
                self.image = pygame.transform.scale(self.image,(50,30))
                self.rect.size = self.image.get_size()
                self.gravity_force = 1500
                self.rect = pygame.Rect(self.rect.x,self.rect.y,50,30)
        else:
            self.image = pygame.transform.scale(self.image,(30,50))
            self.rect.size = self.image.get_size()
            self.rect = pygame.Rect(self.rect.x,self.rect.y,30,50)
            self.gravity_force = 1200

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.groundCheck():
                self.velocity = -350
            if event.key == pygame.K_p:
                self.mode = input("what mode would you like to go to: ")

        if self.mode == "god":
            self.rect = pygame.Rect(self.rect.x,self.rect.y,1,1)


                    
                
    def groundCheck(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            return True
        return False
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        pygame.draw.rect(screen, (255, 0, 0), dino.rect, 2)



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
    def delete(self):
        return 1 
        del self
    
class button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
buttons = [button(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50, "Start Game")]

dino = Dino()
birds = [birds(WIDTH + i * 300, random.randint(50, HEIGHT - 50)) for i in range(5)]
catis = [cati(WIDTH + i * 300, HEIGHT - 15) for i in range(3)]
SAVE = "save.json"
data = {"highscore": 0, "skins": ["default", "cat", "bird"], "current_skin": "default"}
with open(SAVE, "w") as f:
    json.dump(data, f)

def loadScore():
    if os.path.exists(SAVE):
        with open(SAVE, "r") as f:
            data = json.load(f)
            return data.get("highscore", 0)
    else:
        return 0
def saveScore(score):
    data = {"highscore": score}
    with open(SAVE, "w") as f:
        json.dump(data, f)

def GameLoop():
    obsticals = birds + catis
    global dino
    dino = Dino()
    for o in birds + catis:
        o.spawn()
    
    running = True
    total = 0
    while running:


        screen.fill((25, 25, 170))


        dt = pygame.time.Clock().tick(60) / 1000  # Delta time in seconds

        total += dt
        print(total)
        dino.draw(screen) 
        dino.gravity(dt)  # Assuming a frame rate of 60 FPS

        # put all draws before the flip
        for bird in birds:
            bird.velocity[0] = -500  # Move left at 500 pixels per second
            bird.update(dt)
            bird.draw()
            if bird.collision(dino):
                print("Collision detected!")
                running = False
                saveScore(total)
                return  "died"

                # running = False
        for cati in catis:
            cati.velocity[0] = -500  # Move left at 500 pixels per
            cati.update(dt)
            cati.draw()
            if cati.collision(dino):
                print("Collision detected!")
                running = False 
                saveScore(total)
                return "died"
                # running = False

            if bird.collision(dino):
                print("Collision detected!")


        pygame.display.flip()


        for event in pygame.event.get():

            dino.inputhanderler(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f:
                    print(f"Number of birds: {len(birds)}")
                if event.key == pygame.K_c:
                    print(f"Number of cats: {len(catis)}")



def died():
    running = True
    while running:
        screen.fill((255,0,0))
        GameLoop()

        pygame.display.flip()
scene = "game"
while True:
    if scene == "game":
        scene = GameLoop()
    elif scene == "died":
        died()
