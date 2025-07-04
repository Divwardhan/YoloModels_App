from flask import Flask, request, jsonify
import torch
import os
from werkzeug.utils import secure_filename
import uuid
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from models.db import test_connection
from models.user_model import init_db
from routes.user_route import user_bp
from models.db import test_connection

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret")
jwt = JWTManager(app)

init_db()
app.register_blueprint(user_bp)

# Upload settings
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return 'YOLOv5 Flask Backend is Running'


@app.route('/test-db')
def test_db():
    """Check database connectivity by running a simple query."""
    if test_connection():
        return jsonify({'connected': True})
    return jsonify({'connected': False}), 500


if __name__ == '__main__':
    app.run(debug=True)
