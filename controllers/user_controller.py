from flask_jwt_extended import create_access_token
import bcrypt

from models.user_model import create_user, get_user_by_email


def signup_user(email: str, password: str):
    """Handle user signup logic and return status code with payload."""
    if not email or not password:
        return 400, {'message': 'Email and password required'}

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        user_id = create_user(email, hashed.decode('utf-8'))
        return 201, {'id': user_id, 'email': email}
    except Exception:
        return 400, {'message': 'User creation failed'}


def signin_user(email: str, password: str):
    """Handle user signin logic and return status code with payload."""
    if not email or not password:
        return 400, {'message': 'Email and password required'}

    try:
        user = get_user_by_email(email)
        if not user:
            return 401, {'message': 'Invalid credentials'}
        user_id, _, hashed_password = user
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return 401, {'message': 'Invalid credentials'}
        token = create_access_token(identity=user_id)
        return 200, {'access_token': token}
    except Exception:
        return 400, {'message': 'Authentication failed'}
