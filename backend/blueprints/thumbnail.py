import os
import functions as func

from flask import Blueprint, send_from_directory, abort

thumbnail_blueprint = Blueprint('thumbnail', __name__, url_prefix='/api')

@thumbnail_blueprint.route('/thumbnail/<track_id>', methods=['GET'])
def serve_thumbnail(track_id):
    filename = f"{track_id}.jpeg"
    if not os.path.exists(os.path.join(func.IMAGES_DIR, filename)):
        abort(404)
    
    return send_from_directory(func.IMAGES_DIR, filename, mimetype='image/jpeg')