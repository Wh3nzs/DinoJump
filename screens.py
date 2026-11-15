import pygame

from settings import HEIGHT, WIDTH, screen
from ui import buttons, death_buttons
from save_data import active_player, buy_or_equip, data, select_player
from skins import PRICES, SKINS
# ShopBG.png

bacground_image = pygame.image.load("assets/background.png").convert()
bacground_image = pygame.transform.scale(bacground_image, (WIDTH, HEIGHT))

diedscreenBG = pygame.image.load("assets/diedBG.png").convert()
diedscreenBG = pygame.transform.scale(diedscreenBG, (WIDTH, HEIGHT))


MainMenuBG = pygame.image.load("assets/dinoJumpMM.png").convert()
MainMenuBG = pygame.transform.scale(MainMenuBG, (WIDTH, HEIGHT))

ShopBG = pygame.image.load("assets/ShopBG.png").convert()
ShopBG = pygame.transform.scale(ShopBG, (WIDTH, HEIGHT))

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
        player = active_player()
        reward = pygame.font.Font(None, 32).render(
            f"{player['name']} earned {score:.2f} points  |  Balance: {player['points']:.2f}",
            True, "white", "black")
        screen.blit(reward, reward.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

        for button in death_buttons:
            button.draw(screen)
        pygame.display.flip()

def show_start_screen():
    player = data["players"].get(data["active_player"], {})
    name = player.get("name", "")
    replace_name = bool(name)
    focused = True
    hint = "Player name"
    font = pygame.font.Font(None, 32)
    field = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 - 100, 280, 42)
    clock = pygame.time.Clock()
    while True:
        screen.blit(MainMenuBG, (0, 0))
        label = font.render(hint, True, "white", "black")
        screen.blit(label, (field.x, field.y - 30))
        pygame.draw.rect(screen, "black", field)
        pygame.draw.rect(screen, "gold" if focused else "white", field, 2)
        text = font.render(name or "Type your name", True, "white" if name else "gray")
        screen.blit(text, (field.x + 8, field.y + 8))
        for control in buttons:
            control.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            scene = None
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                focused = field.collidepoint(event.pos)
                if focused:
                    replace_name = True
                if buttons[0].is_clicked(event.pos):
                    scene = "game"
                elif buttons[1].is_clicked(event.pos):
                    scene = "shop"
            if event.type == pygame.KEYDOWN and focused:
                if event.key == pygame.K_RETURN:
                    scene = "game"
                elif event.key == pygame.K_BACKSPACE:
                    name = "" if replace_name else name[:-1]
                    replace_name = False
            if event.type == pygame.TEXTINPUT and focused:
                name = (("" if replace_name else name) + event.text)[:12]
                replace_name = False
            if scene:
                if select_player(name):
                    return scene
                hint = "Enter a player name first"
                focused = True
        clock.tick(60)


def show_shop():
    from ui import button

    font = pygame.font.Font(None, 32)
    title = pygame.font.Font(None, 72).render("SHOP", True, "white")
    cards = []
    for name, filename, color in SKINS.values():
        card = pygame.Surface((144, 160))
        card.fill(color)
        sprite = pygame.transform.scale(pygame.image.load(filename).convert_alpha(), (80, 80))
        card.blit(sprite, sprite.get_rect(center=(72, 65)))
        label = font.render(name, True, "white")
        card.blit(label, label.get_rect(center=(72, 112)))
        cards.append(card)

    previous = button(12, HEIGHT // 2 - 25, 50, 50, "<")
    following = button(WIDTH - 62, HEIGHT // 2 - 25, 50, 50, ">")
    play = button(WIDTH // 2 - 100, HEIGHT - 95, 200, 50, "Start Game")
    viewport = pygame.Rect(70, HEIGHT // 2 - 85, WIDTH - 140, 170)
    spacing = viewport.width // 3
    skin_ids = list(SKINS)
    player = active_player()
    equipped = player["skin"]
    message = ""
    selected = skin_ids.index(equipped) if equipped in skin_ids else 0
    equipped = skin_ids[selected]
    visible_cards = []
    direction = 0
    started = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            step = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "start"
                if event.key == pygame.K_RIGHT:
                    step = 1
                elif event.key == pygame.K_LEFT:
                    step = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play.is_clicked(event.pos):
                    return "game"
                if following.is_clicked(event.pos):
                    step = 1
                elif previous.is_clicked(event.pos):
                    step = -1
                else:
                    for rect, skin_id in visible_cards:
                        if rect.collidepoint(event.pos) and skin_id != equipped:
                            if buy_or_equip(skin_id):
                                equipped = skin_id
                                message = ""
                            else:
                                missing = PRICES[skin_id] - player["points"]
                                message = f"You need {missing:.2f} more points for {SKINS[skin_id][0]}."
                            break
            if step and direction == 0:
                direction = step
                started = pygame.time.get_ticks()

        progress = 0.0
        if direction:
            progress = min((pygame.time.get_ticks() - started) / 250, 1.0)
            if progress == 1.0:
                selected = (selected + direction) % len(cards)
                direction = 0
        offset = direction * spacing * progress

        screen.blit(ShopBG, (0,0))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))
        balance = font.render(f"{player['name']}  |  {player['points']:.2f} points", True, "white")
        screen.blit(balance, balance.get_rect(center=(WIDTH // 2, 155)))
        screen.set_clip(viewport)
        visible_cards.clear()
        for slot in range(-2, 3):
            index = (selected + slot) % len(cards)
            card = cards[index]
            x = round(viewport.centerx + slot * spacing - offset)
            rect = card.get_rect(center=(x, viewport.centery))
            screen.blit(card, rect)
            skin_id = skin_ids[index]
            caption = "Owned" if skin_id in player["owned"] else f"{PRICES[skin_id]} points"
            price = font.render(caption, True, "white")
            screen.blit(price, price.get_rect(center=(x, rect.bottom - 18)))
            visible_cards.append((rect.clip(viewport), skin_ids[index]))
            if skin_ids[index] == equipped:
                pygame.draw.rect(screen, "gold", rect, 4)
        screen.set_clip(None)
        status = font.render(message or f"Equipped: {SKINS[equipped][0]}", True, "white")
        screen.blit(status, status.get_rect(center=(WIDTH // 2, viewport.bottom + 38)))
        for control in (previous, following, play):
            control.draw(screen)
        pygame.display.flip()
        clock.tick(60)
