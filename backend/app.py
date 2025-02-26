import os
from flask import Flask, jsonify
from flask_cors import CORS
import functions as func
from blueprints.auth import auth_blueprint
from blueprints.user import user_blueprint
from blueprints.content import content_blueprint
from blueprints.audio import audio_blueprint

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
CORS(app, resources={r'/*': {'origins': '*'}})

# Load initial data from JSON files
func.initDB()

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(content_blueprint)
app.register_blueprint(audio_blueprint)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API server!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)