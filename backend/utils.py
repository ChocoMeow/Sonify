import jwt
import functions as func
from functools import wraps
from flask import jsonify, request, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            current_user_id = data["id"]
            user = func.get_user(current_user_id)
            if not user:
                return jsonify({'message': 'Invalid account!'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired! Please login again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated