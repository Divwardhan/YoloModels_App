from flask import Blueprint, request, jsonify

from controllers.user_controller import signup_user, signin_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    status, payload = signup_user(data.get('email'), data.get('password'))
    return jsonify(payload), status


@user_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json() or {}
    status, payload = signin_user(data.get('email'), data.get('password'))
    return jsonify(payload), status
