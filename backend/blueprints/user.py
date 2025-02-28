import time
import functions as func
from utils import token_required

from flask import Blueprint, jsonify, request

user_blueprint = Blueprint('user', __name__, url_prefix='/api')

@user_blueprint.route('/me', methods=['GET'])
@token_required
def me(current_user_id):
    user = func.USERS.get(current_user_id)
    if not user:
        return jsonify({"message": "User not Found."}), 404
    
    return jsonify({
        "userId": current_user_id,
        "name": user["name"],
        "avatarUrl": user["avatarUrl"],
        "email": user["email"]
    }), 200

@user_blueprint.route('/library', methods=['GET'])
@token_required
def library(current_user_id):
    payload = {
        "tracks": [func.get_track(track_id) for track_id, track in func.TRACKS.items() if track["authorId"] == current_user_id],
        "playlists": [func.get_playlist(playlist_id) for playlist_id, playlist in func.PLAYLISTS.items() if playlist["authorId"] == current_user_id]
    }
    return jsonify(payload), 200

@user_blueprint.route('/createLyrics', methods=['POST'])
@token_required
def createLyrics(current_user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    time.sleep(10)
    prompt, model = data.get("prompt"), data.get("model")
    if not prompt or not model:
        return jsonify({'message': 'Prompt and model are required'}), 400

    return jsonify({
        "lyrics": ""
    }), 200