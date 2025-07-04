from flask import Flask, request, jsonify
import torch
import os
from werkzeug.utils import secure_filename
import uuid

# Initialize Flask app
app = Flask(__name__)

# Upload settings
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return 'YOLOv5 Flask Backend is Running'


if __name__ == '__main__':
    app.run(debug=True)
