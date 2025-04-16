import os
import time
import shutil
import functions as func

from typing import Any
from utils import token_required
from flask import Blueprint, jsonify, request
from gradio_client import Client, handle_file
from mutagen.mp3 import MP3

user_blueprint = Blueprint('user', __name__, url_prefix='/api')

lyrics_prompt = """Generate heartfelt and captivating song lyrics based on the following description:
                    Description: {}
                    Please structure the lyrics into one verse, one chorus, one bridge, and one outro. Focus on evoking strong emotions and vivid imagery. Do not include any titles or introductory text.

                    Format example:
                    [verse]
                    ...

                    [chorus]
                    ...

                    [bridge]
                    ...

                    [outro]
                    ...
                """
@user_blueprint.route('/me', methods=['GET'])
@token_required
def me(current_user_id):
    user = func.USERS.get(current_user_id)
    if not user:
        return jsonify({"message": "User not Found."}), 404
    
    return jsonify({
        "userId": current_user_id,
        "email": user["email"],
        **user
    }), 200

@user_blueprint.route('/library', methods=['GET'])
@token_required
def library(current_user_id):
    payload = {
        "tracks": [func.get_track(track_id) for track_id, track in func.TRACKS.items() if track["authorId"] == current_user_id],
        "playlists": [func.get_playlist(playlist_id) for playlist_id, playlist in func.PLAYLISTS.items() if playlist["authorId"] == current_user_id]
    }
    return jsonify(payload), 200

@user_blueprint.route('/createRandomSongPrompt', methods=['GET'])
@token_required
def createRandomSongPrompt(current_user_id):
    try:
        response = func.request_chatgpt(prompt="Can you give me a random prompt for generating a song on Suno? I’m looking for something creative and unique that could inspire lyrics or a melody. Make it interesting!  Do not include any titles or introductory text i just need the prompt text")
        return jsonify({'prompt': response}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_blueprint.route('/createPlaylist', methods=['POST'])
@token_required
def createPlaylist(current_user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    schema = {
        "name": {"type": str, "required": True},
        "isPrivate": {"type": bool, "required": True}
    }
    if errors := func.validate_input(data, schema):
        return jsonify({"errors": errors}), 400
    
    playlist_id = func.generate_id()
    func.PLAYLISTS[playlist_id] = {
        "tracks": [],
        "name": data["name"],
        "likes": 0,
        "authorId": current_user_id,
        "isPrivate": data["isPrivate"]
    }
    func.update_json(os.path.join("databases", "playlists.json"), func.PLAYLISTS)
    return jsonify({"message": "Playlist created successfully."}), 200

@user_blueprint.route('/updatePlaylist', methods=['POST'])
@token_required
def updatePlaylist(current_user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    schema = {
        "op": {"type": str, "required": True},
        "playlistId": {"type": str, "required": True}
    }
    if errors := func.validate_input(data, schema):
        return jsonify({"errors": errors}), 400

    playlist = func.get_playlist(data["playlistId"])
    if not playlist:
        return jsonify({"errors": {"message": "Playlist not found."}}), 404

    if playlist["authorId"] != current_user_id:
        return jsonify({"errors": {"message": "You don't have permission to access this playlist."}}), 403

    # Handle the specified operation
    operation = data['op']
    if operation == "addTrack":
        track_schema = {"trackId": {"type": str, "required": True}}
        if errors := func.validate_input(data, track_schema):
            return jsonify({"errors": errors}), 400

        playlist["tracks"].append(data["trackId"])
        func.update_json(os.path.join("databases", "playlists.json"), func.PLAYLISTS)
        return jsonify({"message": "Track added successfully."}), 200

    elif operation == "removeTrack":
        track_schema = {"trackId": {"type": str, "required": True}}
        if errors := func.validate_input(data, track_schema):
            return jsonify({"errors": errors}), 400

        try:
            playlist["tracks"].remove(data["trackId"])
            func.update_json(os.path.join("databases", "playlists.json"), func.PLAYLISTS)
            return jsonify({"message": "Track removed successfully."}), 200
        except ValueError:
            return jsonify({"errors": {"message": "Track not found in playlist."}}), 404

    elif operation == "deletePlaylist":
        if data["playlistId"] in func.PLAYLISTS:
            func.PLAYLISTS.pop(data["playlistId"])
            func.update_json(os.path.join("databases", "playlists.json"), func.PLAYLISTS)
            return jsonify({"message": "Playlist deleted successfully."}), 200
        return jsonify({"errors": {"message": "Playlist not found."}}), 404

    return jsonify({"error": "Invalid operation."}), 400

@user_blueprint.route('/generateLyrics', methods=['POST'])
@token_required
def generateLyrics(current_user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    prompt, model = data.get("prompt"), data.get("model")
    if not prompt or not model:
        return jsonify({'message': 'Prompt and model are required'}), 400

    try:
        response = func.request_chatgpt(prompt=lyrics_prompt.format(prompt))
        return jsonify({'lyrics': response}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_blueprint.route('/createTrack', methods=['POST'])
@token_required
def createTrack(current_user_id):
    data: dict[str, Any] = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Initial validation for mode
    MODE_REQUIREMENT = {
        "mode": {
            "type": str,
            "required": True,
            "validator": lambda x: "Invalid mode specified." if x not in ["normal", "custom"] else None
        }
    }
    if errors := func.validate_input(data, MODE_REQUIREMENT):
        return jsonify(errors), 400
    
    mode = data["mode"]
    schema = {
        "mode": MODE_REQUIREMENT["mode"],
        "model": {
            "type": str,
            "required": True
        },
        "isInstrumental": {
            "type": bool,
            "required": True
        }
    }

    if mode == "custom":
        schema.update({
            "title": {
                "type": str,
                "required": True,
                "validator": lambda x: "Title must be at least 20 characters" if len(x) > 20 else None
            },
            "lyrics_input": {
                "type": str,
                "required": True,
                "validator": lambda x: "Lyrics must be at least 3000 characters" if len(x) > 3000 else None
            },
            "genres_input": {
                "type": str,
                "required": True,
                "validator": lambda x: "Genres must be at least 200 characters" if len(x) > 200 else None
            }
        })
    else:
        schema["prompt_input"] = {
            "type": str,
            "required": True,
            "validator": lambda x: "Prompt must be at least 300 characters" if len(x) > 300 else None
        }

    if errors := func.validate_input(data, schema):
        return jsonify({"errors": errors}), 400

    track_id = func.generate_id()
    payload = {
        "mode": mode,
        "model": data["model"],
        "isInstrumental": data["isInstrumental"],
        "vocal_track_prompt": handle_file(func.settings.VOCAL_TRACK_PROMPT_URL),
        "instrumental_track_prompt": handle_file(func.settings.INSTRUMENTAL_TRACK_PROMPT_URL),
        "title": data.get("title", "Untitled Song"),
        "lyrics_input": data.get("lyrics_input"),
        "genres_input": data.get("genres_input")
    }
    
    if mode != "custom":
        payload["title"] = func.request_chatgpt(prompt=f"Generate only a song title for this prompt: {data['prompt_input']}. Do not include any titles or introductory text.")

        # Lyrics Request
        payload["lyrics_input"] = func.request_chatgpt(prompt=lyrics_prompt.format(data['prompt_input']))

        # Genres Request
        payload["genres_input"] = func.request_chatgpt(
            prompt=f"""Generate only song genres for this prompt: {data['prompt_input']}. Do not include any titles or introductory text.
                    Format example: genre1, genre2, genre3, ...
                    """
        )

    try:
        # Generate an image prompt based on lyrics if available
        image_prompt = ""
        image_generated = False
        if payload.get("lyrics_input"):
            image_prompt = func.request_chatgpt(
                prompt=f"""Create a visually striking thumbnail inspired by the following song lyrics: \"{payload['lyrics_input']}\". 
                The thumbnail should capture the emotional essence of the song, featuring vibrant colors and imagery that reflect the themes and mood of the lyrics. 
                Include elements that symbolize happiness and positivity, such as sunshine, flowers, or joyful characters. Ensure the design is eye-catching and suitable for music platforms."""
            )
            
            # Generate and save the image
            image_data = func.generate_image(prompt=image_prompt)
            func.save_image(image_data.get("images", [])[0], filename=f"{track_id}")
            image_generated = True
        
        # Predict song generation
        client = Client(func.settings.YUEGP_API_URL)
        api_params = {
            "run_n_segments": 2,
            "seed": 0,
            "max_new_tokens": 300,
            "vocal_track_prompt": payload["vocal_track_prompt"],
            "instrumental_track_prompt": payload["instrumental_track_prompt"],
            "lyrics_input": payload["lyrics_input"].replace("(", "[").replace(")", "]"),
            "genres_input": payload["genres_input"],
            "prompt_start_time": 0,
            "prompt_end_time": 3,
            "repeat_generation": 1
        }
        
        result = client.predict(api_name="/generate_song", **api_params)
        
        # Format timestamp
        formatted_time = time.strftime("%Y%m%d", time.localtime())

        # Move generated files and determine duration
        track_duration = "Unknown"
        for filename in os.listdir(func.settings.YUEGP_OUTPUT_DIR):
            if filename.startswith(formatted_time):
                source_file = os.path.join(func.settings.YUEGP_OUTPUT_DIR, filename)
                target_file = os.path.join(func.AUDIOS_DIR, f"{track_id}.mp3")
                shutil.move(source_file, target_file)
                
                if filename.endswith(".mp3"):
                    audio = MP3(target_file)
                    track_duration = str(int(audio.info.length // 60)) + ":" + str(int(audio.info.length % 60)).zfill(2)
        
        # Update tracks database
        tracks = func.TRACKS
        tracks[track_id] = {
            "title": payload.get("title", ""),
            "prompt": payload.get("genres_input", ""),
            "lyrics": payload.get("lyrics_input", ""),
            "duration": track_duration,
            "createdTime": time.time(),
            "authorId": current_user_id
        }
        func.update_json(os.path.join("databases", "tracks.json"), tracks)
        
        return jsonify({"message": "Track created successfully", "track_id": track_id, "duration": track_duration}), 201
    
    except Exception as e:
        # Clean up the generated image if track creation failed
        if image_generated:
            func.delete_image(track_id)
        return jsonify({"error": f"Track creation failed: {str(e)}"}), 500

@user_blueprint.route('/removeTrack', methods=['POST'])
@token_required
def remove_track(current_user_id):
    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Define schema for input validation
    schema = {"trackId": {"type": str, "required": True}}
    if errors := func.validate_input(data, schema):
        return jsonify({"errors": errors}), 400
    
    # Fetch the track based on the provided trackId
    track = func.get_track(data["trackId"])
    if not track:
        return jsonify({"error": "Track not found"}), 404
    print(track)
    # Check if the current user is the author of the track
    if track["author"]["id"] != current_user_id:
        return jsonify({"error": "Unauthorized action"}), 403
    
    # Remove the track from the tracks list
    func.TRACKS.pop(track["id"], None)
    func.update_json(os.path.join("databases", "tracks.json"), func.TRACKS)
    
    # Remove associated files from the filesystem
    try:
        os.remove(os.path.join(func.IMAGES_DIR, f"{track['id']}.jpeg"))
        os.remove(os.path.join(func.AUDIOS_DIR, f"{track['id']}.mp3"))
    except Exception as e:
        return jsonify({"message": "Track removed successfully"}), 200
    
    return jsonify({"message": "Track removed successfully"}), 200