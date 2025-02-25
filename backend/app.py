import random, os, datetime, jwt
import functions as func

from functools import wraps
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
CORS(app, resources={r'/*': {'origins': '*'}})

func.initDB()

def get_user(author_id: str) -> dict:
    user = func.USERS.get(author_id)

    if not user:
        return None
    
    return user

def get_track(track_id: str) -> dict:
    track = func.TRACKS.get(track_id)

    if not track:
        return None

    return {
        "id": track["id"],
        "title": track["title"],
        "duration": track["duration"],
        "prompt": track["prompt"],
        "thumbnail": track["thumbnail"],
        "lyrics": track["lyrics"],
        "createdTime": track["createdTime"],
        "author": get_user(track["authorId"]),
        "src": f"http://localhost:5000/api/audio/{track["id"]}"
    }

def get_playlist(playlist_id: str) -> dict:
    playlist = func.PLAYLISTS.get(playlist_id)

    if not playlist:
        return None
    
    random_tracks = random.sample(list(func.TRACKS.values()), 5)

    payload =  {
        "id": playlist["id"],
        "tracks": [get_track(track["id"]) for track in random_tracks],
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
            current_user = data['name']
            
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
    name = data.get('name')
    password = data.get('password')
    if not name or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    users = func.USERS
    if any(user['name'] == name for user in users.values()):
        return jsonify({'message': 'Username already exists'}), 400
    
    user_id = str(len(users.keys()) + 1)
    users[user_id] = {'id': user_id, 'name': name, 'password': generate_password_hash(password), "avatarUrl": "", "active": True}
    func.update_json(os.path.join("db", "users.json"), users)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    if not name or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    users = func.USERS
    for user in users.values():
        if user['name'] == name and check_password_hash(user['password'], password):
            token = jwt.encode({
                'name': name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.secret_key, algorithm='HS256')
            return jsonify({
                'message': 'Login successful',
                'token': token,
                "user": {
                    "name": name,
                    "userId": user["id"],
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
    # request_data = {
    #     "track_id": ""
    # }
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
    # request_data = {
    #     "playlist_id": ""
    # }
    data = request.get_json()
    print(data)
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
    # request_data = {
    #     "track_id": ""
    # }
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

    random_tracks = random.sample(list(func.TRACKS.values()), 5)
    return jsonify({
        "tracks": [get_track(track["id"]) for track in random_tracks]
    }), 200

@app.route('/api/search', methods=['POST'])
@token_required
def search(current_user):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    query = data.get("search_query", "").strip()

    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    tracks = [
        get_track(track["id"]) 
        for track in func.TRACKS.values() 
        if query.lower() in track["title"].lower() or query.lower() in track["prompt"].lower()
    ]

    playlists = [
        get_playlist(playlist["id"]) 
        for playlist in func.PLAYLISTS.values() 
        if query.lower() in playlist["name"].lower()
    ]

    return jsonify({
        "tracks": tracks,
        "playlists": playlists
    }), 200

@app.route('/api/audio/<track_id>')
def serve_audio(track_id):
    filename = f"{track_id}.mp3"
    
    if not os.path.exists(os.path.join(func.AUDIO_DIR, filename)):
        abort(404)
        
    return send_from_directory(func.AUDIO_DIR, filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(port=5000, debug=True)