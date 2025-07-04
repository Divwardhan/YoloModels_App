from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt

from models.user_model import create_user, get_user_by_email

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        user_id = create_user(email, hashed.decode('utf-8'))
        return jsonify({'id': user_id, 'email': email}), 201
    except Exception as exc:
        return jsonify({'message': 'User creation failed'}), 400


@user_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400
    try:
        user = get_user_by_email(email)
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        user_id, _, hashed_password = user
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({'message': 'Invalid credentials'}), 401
        access_token = create_access_token(identity=user_id)
        return jsonify({'access_token': access_token}), 200
    except Exception:
        return jsonify({'message': 'Authentication failed'}), 400

