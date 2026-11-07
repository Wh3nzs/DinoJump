import pygame, random, json, os

from pygame import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dino jump")
pygame.display.set_icon(pygame.image.load("assets/dino.png"))

score_font = pygame.font.SysFont("fixed", 30)


font = pygame.font.Font(None, 36)
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
data = {"highscore": 0, "Name": "None", "current_skin": "default"}

# Load the existing save instead of wiping it every launch
if os.path.exists(SAVE):
    try:
        with open(SAVE, "r") as f:
            data.update(json.load(f))
    except (json.JSONDecodeError, OSError):
        pass


def loadScore():
    return data.get("highscore", 0)


def save(score, name):
    data["highscore"] = score
    data["Name"] = name
    with open(SAVE, "w") as f:
        json.dump(data, f)


def ask_name(prompt="New high score! Enter your name:", max_len=12):
    pygame.event.clear()  # drop any leftover keypresses from gameplay
    clock = pygame.time.Clock()
    name_font = pygame.font.Font(None, 56)
    prompt_font = pygame.font.Font(None, 40)
    name = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() or "None"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode and event.unicode.isprintable() and len(name) < max_len:
                    name += event.unicode

        screen.fill((30, 30, 30))

        prompt_surf = prompt_font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_surf, prompt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))

        # blinking cursor
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        name_surf = name_font.render(name + cursor, True, (255, 255, 0))
        screen.blit(name_surf, name_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(60)


bacground_image = pygame.image.load("assets/background.png").convert()
bacground_image = pygame.transform.scale(bacground_image, (WIDTH, HEIGHT))

diedscreenBG = pygame.image.load("assets/diedBG.png").convert()
diedscreenBG = pygame.transform.scale(diedscreenBG, (WIDTH, HEIGHT))

def GameLoop():
    obsticals = birds + catis
    global dino
    dino = Dino()
    for o in birds + catis:
        o.spawn()
    
    running = True
    total = 0
    while running:


        screen.blit(bacground_image, (0,0))


        dt = pygame.time.Clock().tick(60) / 1000  # Delta time in seconds
        import math
        total += dt
        total = round(total, 2)
        global score
        score = total
        dino.draw(screen) 
        dino.gravity(dt)  # Assuming a frame rate of 60 FPS
        dino.update()

        # put all draws before the flip
        for bird in birds:
            bird.velocity[0] = -500  # Move left at 500 pixels per second
            bird.update(dt)
            bird.draw()
            if bird.collision(dino):
                running = False
                if data["highscore"] < total:
                    save(total, ask_name())
                return "died"

        for cati in catis:
            cati.velocity[0] = -500  # Move left at 500 pixels per second
            cati.update(dt)
            cati.draw()
            if cati.collision(dino):
                running = False 
                if data["highscore"] < total:
                    save(total, ask_name())
                return "died"


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
    font = pygame.font.Font(None, 72)
    dead_text = font.render("YOU DIED " + "Score: " + str(score), True, (0, 0, 0))
    text_rect = dead_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    font = pygame.font.Font(None, 72)
    highScore_text = font.render("High score: " + str(data["highscore"]) + " by " + data["Name"], True, (0, 0, 0))
    highscoreRect = highScore_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

    while True:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return "game"
        screen.blit(diedscreenBG, (0, 0))
        screen.blit(dead_text, text_rect)
        screen.blit(highScore_text, highscoreRect)
        pygame.display.flip()

scene = "game"
while True:
    if scene == "game":
        scene = GameLoop()
    elif scene == "died":
        scene = died()