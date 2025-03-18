import os
import json
import random
import uuid

# Define directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, 'db')
AUDIOS_DIR = os.path.join(ROOT_DIR, 'audios')
IMAGES_DIR = os.path.join(ROOT_DIR, 'images')

USERS = {}
TRACKS = {}
PLAYLISTS = {}

class Settings:
    def __init__(self):
        self.SECRET_KEY: str = ""
        self.HOST: str = "0.0.0.0"
        self.PORT: int = 5000
        self.OLLAMA_API_URL: str = ""
        self.OLLAMA_MODEL: str = ""
        self.YUEGP_API_URL: str = ""
        self.YUEGP_OUTPUT_DIR: str = ""
        self.STABLE_DIFFUSION_API_URL: str = ""
    
    def load(self) -> None:
        settings: dict = load_json("settings.json")
        self.SECRET_KEY: str = settings.get("SECRET_KEY")
        self.HOST: str = settings.get("HOST")
        self.PORT: int = settings.get("PORT")
        self.OLLAMA_API_URL: str = settings.get("OLLAMA_API_URL")
        self.OLLAMA_MODEL: str = settings.get("OLLAMA_MODEL")
        self.YUEGP_API_URL: str = settings.get("YUEGP_API_URL")
        self.YUEGP_OUTPUT_DIR: str = settings.get("YUEGP_OUTPUT_DIR")
        self.STABLE_DIFFUSION_API_URL: str = settings.get("STABLE_DIFFUSION_API_URL")

settings: Settings = Settings()

# Load data from JSON files
def load_json(file_path: setattr) -> dict:
    with open(os.path.join(ROOT_DIR, file_path), encoding="utf8") as json_file:
            return json.load(json_file)

def update_json(file_path: str, data: dict) -> None:
    with open(os.path.join(ROOT_DIR, file_path), 'w') as f:
        json.dump(data, f, indent=4)

def initDB():
    global USERS, TRACKS, PLAYLISTS
    USERS = load_json(os.path.join(DB_DIR, 'users.json'))
    TRACKS = load_json(os.path.join(DB_DIR, 'tracks.json'))
    PLAYLISTS = load_json(os.path.join(DB_DIR, 'playlists.json'))

def generate_id() -> str:
    unique_id = str(uuid.uuid4())[:8]
    return unique_id

def get_user(user_id: str) -> dict:
    user = USERS.get(user_id)
    if not user:
        return None
    return {
        "id": user_id,
        "name": user["name"],
        "avatarUrl": user["avatarUrl"]
    }

def get_track(track_id: str) -> dict:
    track = TRACKS.get(track_id)
    if not track:
        return None
    return {
        "id": track_id,
        "title": track["title"],
        "duration": track["duration"],
        "prompt": track["prompt"],
        "thumbnail": track["thumbnail"],
        "lyrics": track["lyrics"],
        "createdTime": track["createdTime"],
        "author": get_user(track["authorId"]),
        "src": f"http://127.0.0.1:5000/api/audio/{track_id}"
    }

def get_playlist(playlist_id: str) -> dict:
    playlist = PLAYLISTS.get(playlist_id)
    if not playlist:
        return None
    random_track_ids = random.sample(list(TRACKS.keys()), 5)
    payload = {
        "id": playlist_id,
        "tracks": [get_track(track_id) for track_id in random_track_ids],
        "name": playlist["name"],
        "likes": playlist["likes"],
        "author": get_user(playlist["authorId"]),
        "type": "Playlist"
    }
    payload["totalSongs"] = len(payload["tracks"])
    return payload