from datetime import datetime

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from flask_jwt_extended import JWTManager, create_access_token

auth_bp = Blueprint('auth', __name__)

# Initialize Flask-JWT-Extended
jwt = JWTManager()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username is already taken'}), 409

    new_user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user and check_password_hash(user.password_hash, data.get('password')):
        # Create JWT token
        access_token = create_access_token(identity={'user_id': user.id}, expires_delta=datetime.timedelta(hours=24))

        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid username or password'}), 401
