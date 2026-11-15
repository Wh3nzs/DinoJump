import pygame

from settings import screen
from player import Dino
from obstacles import birds, catis
from screens import bacground_image
from save_data import finish_run

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
                finish_run(total)
                return "died"

        for cati in catis:
            cati.velocity[0] = -500  # Move left at 500 pixels per second
            cati.update(dt)
            cati.draw()
            if cati.collision(dino):
                finish_run(total)
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




