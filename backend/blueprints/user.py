from flask import Blueprint, jsonify
from utils import token_required
import functions as func
import time

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
    time.sleep(5)  # Simulate delay as in original code
    payload = {
        "tracks": [func.get_track(track_id) for track_id, track in func.TRACKS.items() if track["authorId"] == current_user_id],
        "playlists": [func.get_playlist(playlist_id) for playlist_id, playlist in func.PLAYLISTS.items() if playlist["authorId"] == current_user_id]
    }
    return jsonify(payload), 200