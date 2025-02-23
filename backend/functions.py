import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(ROOT_DIR, 'audio_files')

USERS = {}
TRACKS = {}
PLAYLISTS = {}

def open_json(path: str) -> dict:
    try:
        with open(os.path.join(ROOT_DIR, path), encoding="utf8") as json_file:
            return json.load(json_file)
    except:
        return {}

def update_json(path: str, new_data: dict) -> None:
    data = open_json(path)
    if not data:
        return
    
    data.update(new_data)

    with open(os.path.join(ROOT_DIR, path), "w") as json_file:
        json.dump(data, json_file, indent=4)

def initDB() -> None:
    global USERS, TRACKS, PLAYLISTS
    
    USERS = open_json(os.path.join('db', 'users.json'))
    TRACKS = open_json(os.path.join('db', 'tracks.json'))
    PLAYLISTS = open_json(os.path.join('db', 'playlists.json'))