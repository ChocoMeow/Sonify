from flask import Blueprint, jsonify, request
import functions as func
import random
import time

content_blueprint = Blueprint('content', __name__, url_prefix='/api')

@content_blueprint.route('/popular', methods=['GET'])
def popular():
    time.sleep(5)  # Simulate delay as in original code
    return jsonify({
        "tracks": [func.get_track(track) for track in func.TRACKS.keys()],
        "playlists": [func.get_playlist(playlist) for playlist in func.PLAYLISTS.keys()]
    }), 200

@content_blueprint.route('/track', methods=['POST'])
def track():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    track = func.get_track(data.get("track_id"))
    if not track:
        return jsonify({
            "error": {
                "status": 404,
                "message": "Resource not found."
            }
        }), 404
    return jsonify(track), 200

@content_blueprint.route('/playlist', methods=['POST'])
def playlist():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    playlist = func.get_playlist(data.get("playlist_id"))
    if not playlist:  # Fixed typo from 'track' to 'playlist'
        return jsonify({
            "error": {
                "status": 404,
                "message": "Resource not found."
            }
        }), 404
    return jsonify(playlist), 200

@content_blueprint.route('/similar', methods=['POST'])
def similar():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    time.sleep(5)  # Simulate delay as in original code
    track = func.get_track(data.get("track_id"))
    if not track:
        return jsonify({
            "error": {
                "status": 404,
                "message": "Resource not found."
            }
        }), 404
    random_track_ids = random.sample(list(func.TRACKS.keys()), 7)
    return jsonify({
        "tracks": [func.get_track(track_id) for track_id in random_track_ids]
    }), 200

@content_blueprint.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    time.sleep(5)  # Simulate delay as in original code
    query = data.get("search_query", "").strip()
    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    tracks = [
        func.get_track(track_id)
        for track_id, track in func.TRACKS.items() 
        if query.lower() in track["title"].lower() or query.lower() in track["prompt"].lower()
    ]
    playlists = [
        func.get_playlist(playlist_id)
        for playlist_id, playlist in func.PLAYLISTS.items() 
        if query.lower() in playlist["name"].lower()
    ]
    return jsonify({
        "tracks": tracks,
        "playlists": playlists
    }), 200