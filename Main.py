from gameplay import GameLoop
from screens import died, show_shop, show_start_screen

scene = "start"
while True:
    if scene == "game":
        scene = GameLoop()
    elif scene == "died":
        scene = died()
    elif scene == "start":
        scene = show_start_screen()
    elif scene == "shop":
        scene = show_shop()