import os
import functions as func

from flask import Blueprint, send_from_directory, abort

audio_blueprint = Blueprint('audio', __name__, url_prefix='/api')

@audio_blueprint.route('/audio/<track_id>', methods=['GET'])
def serve_audio(track_id):
    filename = f"{track_id}.mp3"
    if not os.path.exists(os.path.join(func.AUDIOS_DIR, filename)):
        abort(404)
    return send_from_directory(func.AUDIOS_DIR, filename, mimetype='audio/mpeg')