import json

FPS = 60
TILEZISE = 64

ANCHO = 1200
CONFIG_FILE_PATH = './configs/config.json'

def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)

