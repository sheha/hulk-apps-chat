from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fijubriju'

    socketio.init_app(app)

    # Import and register Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Placeholder for chat blueprint registration
    # from .chat import chat_bp
    # app.register_blueprint(chat_bp)

    return app

