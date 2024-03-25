import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
import redis

db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Ensure all required environment variables are set
    if not all(os.getenv(key) for key in
               ['SECRET_KEY', 'DATABASE_URI', 'SQLALCHEMY_TRACK_MODIFICATIONS', 'JWT_SECRET_KEY', 'CORS_ORIGINS',
                'REDIS_URL']):
        raise EnvironmentError("Critical configuration is missing in environment variables.")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    cors_origins = os.getenv('CORS_ORIGINS')

    # Redis configuration for Flask-Session
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url(os.getenv('REDIS_URL'))

    Session(app)  # Initialize Flask-Session here
    CORS(app, resources={r"/*": {"origins": cors_origins}})
    socketio.init_app(app, cors_allowed_origins=cors_origins)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app, socketio
