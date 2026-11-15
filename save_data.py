import json
import os

from skins import PRICES, SKINS

SAVE = "save.json"
data = {"highscore": 0, "Name": "None", "players": {}, "active_player": ""}
if os.path.exists(SAVE):
    try:
        with open(SAVE, encoding="utf-8") as file:
            data.update(json.load(file))
    except (json.JSONDecodeError, OSError):
        pass


def write_save():
    with open(SAVE + ".tmp", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    os.replace(SAVE + ".tmp", SAVE)


def active_player():
    return data["players"][data["active_player"]]


def select_player(name):
    name = name.strip()
    if not name:
        return False
    key = name.casefold()
    players = data["players"]
    if key not in players:
        # Carry the previously shared skin into the first named profile.
        skin = data.get("current_skin", "default") if not players else "default"
        owned = ["default"]
        if skin in SKINS and skin != "default":
            owned.append(skin)
        players[key] = {"name": name, "points": 0, "owned": owned, "skin": owned[-1]}
    data["active_player"] = key
    write_save()
    return True


def finish_run(score):
    player = active_player()
    player["points"] = round(player["points"] + score, 2)
    if score > data["highscore"]:
        data["highscore"] = score
        data["Name"] = player["name"]
    write_save()


def buy_or_equip(skin):
    player = active_player()
    if skin not in player["owned"]:
        price = PRICES[skin]
        if player["points"] < price:
            return False
        player["points"] = round(player["points"] - price, 2)
        player["owned"].append(skin)
    player["skin"] = skin
    write_save()
    return True
