import random, os, datetime, jwt, uuid
import functions as func

from functools import wraps
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
CORS(app, resources={r'/*': {'origins': '*'}})

func.initDB()

def generate_id() -> str:
    unique_id = str(uuid.uuid4())[:8]
    return unique_id

def get_user(user_id: str) -> dict:
    user = func.USERS.get(user_id)

    if not user:
        return None
    
    return {
        "id": user_id,
        "name": user["name"],
        "avatarUrl": user["avatarUrl"]
    }

def get_track(track_id: str) -> dict:
    track = func.TRACKS.get(track_id)

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
        "src": f"http://localhost:5000/api/audio/{track_id}"
    }

def get_playlist(playlist_id: str) -> dict:
    playlist = func.PLAYLISTS.get(playlist_id)

    if not playlist:
        return None
    
    random_track_ids = random.sample(list(func.TRACKS.keys()), 5)
    payload =  {
        "id": playlist_id,
        "tracks": [get_track(track_id) for track_id in random_track_ids],
        "name": playlist["name"],
        "likes": playlist["likes"],
        "author": get_user(playlist["authorId"]),
        "type": "Playlist"
    }

    payload["totalSongs"] = len(payload["tracks"])
    return payload

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.secret_key, algorithms=["HS256"])
            current_user = data['id']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API server!"})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    if not email or not name or not password:
        return jsonify({'message': 'Email, name and password required'}), 400
    
    users = func.USERS
    if any(user['email'] == email.lower() for user in users.values()):
        return jsonify({'message': 'Email already exists'}), 400
    
    user_id = generate_id()
    users[user_id] = {'name': name, 'email': email.lower(), 'password': generate_password_hash(password), "avatarUrl": "", "active": True}
    func.update_json(os.path.join("db", "users.json"), users)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email: str = data.get('email')
    password: str = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400
    
    users = func.USERS
    for user_id, user in users.items():
        if user['email'] == email.lower() and check_password_hash(user['password'], password):
            token = jwt.encode({
                'id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.secret_key, algorithm='HS256')
            return jsonify({
                'message': 'Login successful',
                'token': token,
                "user": {
                    "userId": user_id,
                    "email": user["email"],
                    "name": user["name"],
                    "avatarUrl": user["avatarUrl"]
                }
            }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/popular', methods=['GET'])
def popular():
    return jsonify({
        "tracks": [get_track(track) for track in func.TRACKS.keys()],
        "playlists": [get_playlist(playlist) for playlist in func.PLAYLISTS.keys()]
    }), 200

@app.route('/api/track', methods=['POST'])
def track():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    track = get_track(data.get("track_id"))
    if not track:
        return jsonify({
            "error": {
                "status": 404,
                "message": "Resource not found."
            }
        }), 404

    return jsonify(track), 200

@app.route('/api/playlist', methods=['POST'])
def playlist():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    playlist = get_playlist(data.get("playlist_id"))
    if not track:
        return jsonify({
            "error": {
                "status": 404,
                "message": "Resource not found."
            }
        }), 404

    return jsonify(playlist), 200

@app.route('/api/similar', methods=['POST'])
def similar():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    track = get_track(data.get("track_id"))
    if not track:
        return jsonify({
            "error": {
                "status": 404,
                "message": "Resource not found."
            }
        }), 404

    random_track_ids = random.sample(list(func.TRACKS.keys()), 7)
    return jsonify({
        "tracks": [get_track(track_id) for track_id in random_track_ids]
    }), 200

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    query = data.get("search_query", "").strip()

    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    tracks = [
        get_track(track_id)
        for track_id, track in func.TRACKS.items() 
        if query.lower() in track["title"].lower() or query.lower() in track["prompt"].lower()
    ]

    playlists = [
        get_playlist(playlist_id)
        for playlist_id, playlist in func.PLAYLISTS.items() 
        if query.lower() in playlist["name"].lower()
    ]

    return jsonify({
        "tracks": tracks,
        "playlists": playlists
    }), 200

@app.route('/api/audio/<track_id>', methods=['GET'])
def serve_audio(track_id):
    filename = f"{track_id}.mp3"
    
    if not os.path.exists(os.path.join(func.AUDIO_DIR, filename)):
        abort(404)
        
    return send_from_directory(func.AUDIO_DIR, filename, mimetype='audio/mpeg')

@app.route("/api/library", methods=['GET'])
@token_required
def library(current_user) -> None:
    payload = {
        "tracks": [get_track(track_id) for track_id, track in func.TRACKS.items() if track["authorId"] == current_user],
        "playlists": [get_playlist(playlist_id) for playlist_id, playlist in func.PLAYLISTS.items() if playlist["authorId"] == current_user]
    }

    return jsonify(payload), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)