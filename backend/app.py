import random
import functions as func

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
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
        "author": get_user(track["authorId"])
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

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API server!"})

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
def search():
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)