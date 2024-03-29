import os
import redis
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session

db = SQLAlchemy()
socketio = SocketIO()

# Initialize Flask-Limiter, general use limiter for requests but not for socket operations
# limiter = Limiter(
#     key_func=get_remote_address,  # Use the remote address as the key for rate limiting
#     default_limits=["10 per minute", "300 per day"]  # Default rate limits
# )
# redis client for other uses other than user session management
redis_client = None


def create_app():
    app = Flask(__name__)

    global redis_client
    # Ensure all required environment variables are set
    if not all(os.getenv(key) for key in
               ['SECRET_KEY', 'DATABASE_URI', 'SQLALCHEMY_TRACK_MODIFICATIONS', 'JWT_SECRET_KEY', 'CORS_ORIGINS',
                'REDIS_URL']):
        raise EnvironmentError("Critical configuration is missing in environment variables.")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_URL'), decode_responses=True)

    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    cors_origins = os.getenv('CORS_ORIGINS')
    print(cors_origins)

    # Redis configuration for Flask-Session
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url(os.getenv('REDIS_URL'))

    Session(app)  # Initialize Flask-Session here
    CORS(app, resources={r"/*": {"origins": cors_origins}})
    socketio.init_app(app, cors_allowed_origins=cors_origins)

    # limiter.init_app(app)

    db.init_app(app)

    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    from .models import User, Message
    with app.app_context():
        db.create_all()

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .chat import chat_bp
    app.register_blueprint(chat_bp)

    return app
