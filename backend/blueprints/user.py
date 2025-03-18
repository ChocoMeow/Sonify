import os
import time
import shutil
import functions as func

from utils import token_required
from flask import Blueprint, jsonify, request
from gradio_client import Client, handle_file
from mutagen.mp3 import MP3

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
        response = func.request_chatgpt(
            prompt=f"""Generate emotional and engaging lyrics for a song based on the following description:
                    Description: {prompt}
                    Include verses, a chorus, and a bridge. Do not include any titles or introductory text.
                    """
        )
        return jsonify({'lyrics': response}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_blueprint.route('/createTrack', methods=['POST'])
@token_required
def createTrack(current_user_id):
    if not os.path.exists(func.settings.YUEGP_OUTPUT_DIR):
        return jsonify({"error": "Output directory is not set"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    mode = data.get("mode", "").strip().lower()
    if not mode:
        return jsonify({"error": "Mode is required"}), 400
    
    if mode not in ['normal', 'custom']:
        return jsonify({"error": "Invalid mode specified"}), 400
    
    required_fields = ["model", "isInstrumental"]
    if mode == "custom":
        required_fields.extend(["lyrics_input", "title", "genres_input"])
    else:
        required_fields.append("prompt_input")
    
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    track_id = func.generate_id()
    
    payload = {
        "mode": mode,
        "model": data["model"],
        "isInstrumental": data["isInstrumental"],
        "vocal_track_prompt": handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
        "instrumental_track_prompt": handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav')
    }
    
    if mode == 'custom':
        payload.update({
            "lyrics_input": data["lyrics_input"],
            "title": data["title"],
            "genres_input": data["genres_input"]
        })
    else:
        payload.update({
            "prompt_input": data["prompt_input"]
        })
        
        # Generate title and lyrics using request_chatgpt
        generated_data = func.request_chatgpt(
            prompt=f"Generate a song title and lyrics based on this prompt: {payload['prompt_input']}"
        )
        payload["title"] = generated_data.get("title", "Untitled Song")
        payload["lyrics_input"] = generated_data.get("lyrics", "")
    
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
            func.save_image(image_data.get("images", [])[0], filename=f"{track_id}.jpeg")
        
        # Format timestamp
        formatted_time = time.strftime("%Y%m%d-%H%M-%S", time.localtime())
        
        # Predict song generation
        client = Client(func.settings.YUEGP_API_URL)
        api_params = {
            "model": payload["model"],
            "isInstrumental": payload["isInstrumental"],
            "run_n_segments": 2,
            "seed": 0,
            "max_new_tokens": 300,
            "vocal_track_prompt": payload["vocal_track_prompt"],
            "instrumental_track_prompt": payload["instrumental_track_prompt"],
            "prompt_start_time": 0,
            "prompt_end_time": 3,
            "repeat_generation": 1
        }
        
        if mode == 'custom':
            api_params.update({
                "lyrics_input": payload["lyrics_input"],
                "genres_input": payload["genres_input"]
            })
        else:
            api_params.update({
                "prompt_input": payload["prompt_input"]
            })
        
        result = client.predict(api_name="/generate_song", **api_params)
        
        # Move generated files and determine duration
        track_duration = "Unknown"
        for filename in os.listdir(func.settings.YUEGP_OUTPUT_DIR):
            if filename.startswith(formatted_time):
                source_file = os.path.join(func.settings.YUEGP_OUTPUT_DIR, filename)
                target_file = os.path.join(func.AUDIOS_DIR, filename)
                shutil.move(source_file, target_file)
                
                if filename.endswith(".mp3"):
                    audio = MP3(target_file)
                    track_duration = str(int(audio.info.length // 60)) + ":" + str(int(audio.info.length % 60)).zfill(2)
        
        # Update tracks database
        tracks = func.TRACKS
        tracks[track_id] = {
            "title": payload.get("title", ""),
            "duration": track_duration,
            "prompt": payload.get("genres_input" if mode == 'custom' else "prompt_input", ""),
            "lyrics": payload.get("lyrics_input", ""),
            "createdTime": time.time(),
            "authorId": current_user_id
        }
        func.update_json(os.path.join("db", "tracks.json"), tracks)
        
        return jsonify({"message": "Track created successfully", "track_id": track_id, "duration": track_duration}), 201
    
    except Exception as e:
        return jsonify({"error": f"Track creation failed: {str(e)}"}), 500