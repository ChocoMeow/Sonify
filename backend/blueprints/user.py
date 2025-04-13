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
        "title": data.get("title"),
        "lyrics_input": data.get("lyrics_input"),
        "genres_input": data.get("genres_input")
    }
    
    if mode != "custom":
        generated_title = func.request_chatgpt(prompt=f"Generate only a song title for this prompt: {data['prompt_input']}. Do not include any titles or introductory text.")
        payload["title"] = generated_title.strip() if generated_title else "Untitled Song"

        # Lyrics Request
        generated_lyrics = func.request_chatgpt(prompt=lyrics_prompt.format(data['prompt_input']))
        payload["lyrics_input"] = generated_lyrics.strip() if generated_lyrics else ""

        # Genres Request
        generated_genres = func.request_chatgpt(prompt=f"Generate only song genres for this prompt: {data['prompt_input']}. Do not include any titles or introductory text.")
        payload["genres_input"] = generated_genres.replace("Genre:", "").strip() if generated_genres else ""      
    
    try:
        # Generate an image prompt based on lyrics if available
        image_prompt = ""
        if payload.get("lyrics_input"):
            image_prompt = func.request_chatgpt(
                prompt=f"""Create a visually striking thumbnail inspired by the following song lyrics: \"{payload['lyrics_input']}\". 
                The thumbnail should capture the emotional essence of the song, featuring vibrant colors and imagery that reflect the themes and mood of the lyrics. 
                Include elements that symbolize happiness and positivity, such as sunshine, flowers, or joyful characters. Ensure the design is eye-catching and suitable for music platforms."""
            )
            
            # Generate and save the image
            image_data = func.generate_image(prompt=image_prompt)
            func.save_image(image_data.get("images", [])[0], filename=f"{track_id}")
        
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
        return jsonify({"error": f"Track creation failed: {str(e)}"}), 500