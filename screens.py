import pygame

from settings import HEIGHT, WIDTH, screen
from ui import buttons, death_buttons
from save_data import data

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


MainMenuBG = pygame.image.load("assets/dinoJumpMM.png").convert()
MainMenuBG = pygame.transform.scale(MainMenuBG, (WIDTH, HEIGHT))
def died():
    from gameplay import score

    running = True
    font = pygame.font.Font(None, 72)
    dead_text = font.render("YOU DIED " + "Score: " + str(score), True, (0, 0, 0))
    text_rect = dead_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    font = pygame.font.Font(None, 72)
    highScore_text = font.render("High score: " + str(data["highscore"]) + " by " + data["Name"], True, (0, 0, 0))
    highscoreRect = highScore_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if death_buttons[0].is_clicked(event.pos):
                    return "game"
                if death_buttons[1].is_clicked(event.pos):
                    return "shop"
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    running = False
                    return "game"
        screen.blit(diedscreenBG, (0, 0))
        screen.blit(dead_text, text_rect)
        screen.blit(highScore_text, highscoreRect)

        for button in death_buttons:
            button.draw(screen)
        pygame.display.flip()

def show_start_screen():
    running = True
    while running:
        screen.blit(MainMenuBG, (0, 0))
        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].is_clicked(event.pos):
                    return "game"
                if buttons[1].is_clicked(event.pos):
                    return "shop"

        pygame.display.flip()

def show_shop():
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen with black
        font = pygame.font.Font(None, 72)
        shop_text = font.render("SHOP", True, (255, 255, 255))
        text_rect = shop_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(shop_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to return to the main menu
                    return "start"

        pygame.display.flip()

