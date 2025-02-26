import os
import json
import random
import uuid

# Define directories
DB_DIR = os.path.join(os.path.dirname(__file__), 'db')
AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'audio')

USERS = {}
TRACKS = {}
PLAYLISTS = {}

# Load data from JSON files
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def update_json(file_path, data):
    with open(file_path, 'w') as f:
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