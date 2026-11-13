import json
import os

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


