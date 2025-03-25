import os
import json
import random
import uuid
import base64
import requests

from urllib.parse import urljoin
from typing import Any

# Define directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, 'databases')
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
        self.VOCAL_TRACK_PROMPT_URL: str = ""
        self.INSTRUMENTAL_TRACK_PROMPT_URL: str = ""
    
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
        self.VOCAL_TRACK_PROMPT_URL: str = settings.get("VOCAL_TRACK_PROMPT_URL")
        self.INSTRUMENTAL_TRACK_PROMPT_URL: str = settings.get("INSTRUMENTAL_TRACK_PROMPT_URL")

        if not os.path.exists(self.YUEGP_OUTPUT_DIR):
            raise FileNotFoundError(f"The YUE output directory '{self.YUEGP_OUTPUT_DIR}' does not exist.")

settings: Settings = Settings()

def load_json(file_path: str) -> dict:
    file_path_full = os.path.join(ROOT_DIR, file_path)
    
    # Check if the file exists
    if not os.path.exists(file_path_full):
        with open(file_path_full, 'w') as f:
            json.dump({}, f, indent=4)

    # Now read from the file
    with open(file_path_full, encoding="utf8") as json_file:
        return json.load(json_file)

def update_json(file_path: str, data: dict) -> None:
    with open(os.path.join(ROOT_DIR, file_path), 'w') as f:
        json.dump(data, f, indent=4)

def save_image(bytes: str, filename: str) -> None:
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    image_data = base64.b64decode(bytes)
    with open(os.path.join(IMAGES_DIR, f"{filename}.jpeg"), "wb") as f:
        f.write(image_data)

def initDB() -> None:
    global USERS, TRACKS, PLAYLISTS
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    if not os.path.exists(AUDIOS_DIR):
        os.makedirs(AUDIOS_DIR)

    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

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

def generate_image(prompt: str, seed: int = None, steps: int = 50, width: int = 512, height: int = 512) -> dict | None:
    response = requests.post(
        url=urljoin(settings.STABLE_DIFFUSION_API_URL, "/sdapi/v1/txt2img"),
        headers={"Content-Type": "application/json"},
        json={
            "prompt": prompt,
            "seed": seed,
            "steps": steps,
            "width": width,
            "height": height
        })

    response.raise_for_status()
    return response.json()

def request_chatgpt(prompt: str) -> str:
    payload = {
        'prompt': prompt,
        'model': settings.OLLAMA_MODEL
    }
    
    response = requests.post(
        url=urljoin(settings.OLLAMA_API_URL, "/api/generate"),
        headers={'Content-Type': 'application/json'},
        json=payload,
        stream=True  # Stream the response
    )
    response.raise_for_status()
    
    all_responses = []

    # Process the streamed response
    for line in response.iter_lines():
        if line:  # Ensure the line is not empty
            decoded_line = line.decode('utf-8')
            try:
                json_data = json.loads(decoded_line)
                all_responses.append(json_data['response'])
            except json.JSONDecodeError:
                print(f"Failed to decode line: {decoded_line}")

    # Join all parts into a complete response
    return ''.join(all_responses)
    
def validate_field(data: dict[str, Any], field: str, rules: dict[str, Any]) -> str | None:
    """
    Validate a single field based on the provided rules.

    Args:
        data: The input data dictionary.
        field: The field name to validate.
        rules: A dictionary of validation rules for the field.

    Returns:
        An error message (str) if validation fails, or None if it passes.
    """
    # Check if the field is missing or None
    if field not in data or data[field] is None:
        if rules.get("required", True):
            return f"{field} is required"
        return None

    value = data[field]
    
    # Type validation
    expected_type = rules.get("type")
    if expected_type and not isinstance(value, expected_type):
        return f"{field} must be a {expected_type.__name__}"

    # Special case for strings: check for emptiness
    if expected_type == str and not rules.get("allow_empty", True) and not value.strip():
        return f"{field} cannot be empty"

    # Custom validator function
    custom_validator = rules.get("validator")
    if custom_validator and callable(custom_validator):
        error = custom_validator(value)
        if error:
            return error

    return None

def validate_input(data: dict[str, Any], schema: dict[str, dict[str, Any]]) -> dict[str, str]:
    """
    Validate input data based on the provided schema.

    Args:
        data: The input data dictionary to validate.
        schema: A dictionary mapping field names to their validation rules.

    Returns:
        A dictionary of field names mapped to error messages. Empty if all validations pass.
    """
    errors = {}
    for field, rules in schema.items():
        error = validate_field(data, field, rules)
        if error:
            errors[field] = error
    return errors