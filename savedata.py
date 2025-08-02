import json
import os

SAVE_FILE = "save_game.json"


def save_data(data):
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)


def load_data():
    if not os.path.exists(SAVE_FILE):
        return {"best_time": 0, "last_score": 0}
    with open(SAVE_FILE, 'r') as f:
        return json.load(f)
