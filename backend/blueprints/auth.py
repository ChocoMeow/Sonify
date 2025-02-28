import os
import jwt
import datetime
import functions as func

from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api')

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    if not email or not name or not password:
        return jsonify({'message': 'Email, name and password required'}), 400
    
    users = func.USERS
    if any(user['email'] == email.lower() for user in users.values()):
        return jsonify({'message': 'Email already exists'}), 400
    
    user_id = func.generate_id()
    users[user_id] = {
        'name': name,
        'email': email.lower(),
        'password': generate_password_hash(password),
        "avatarUrl": "",
        "active": True
    }
    func.update_json(os.path.join("db", "users.json"), users)

    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400
    
    users = func.USERS
    for user_id, user in users.items():
        if user['email'] == email.lower() and check_password_hash(user['password'], password):
            access_token = jwt.encode({
                'id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.secret_key, algorithm='HS256')
            refresh_token = jwt.encode({
                'id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, current_app.secret_key, algorithm='HS256')
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_blueprint.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing!'}), 400
    
    try:
        decoded = jwt.decode(refresh_token, current_app.secret_key, algorithms=["HS256"])
        user_id = decoded['id']
        new_access_token = jwt.encode({
            'id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.secret_key, algorithm='HS256')
        return jsonify({
            'message': 'Token refreshed',
            'access_token': new_access_token
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token!'}), 401