from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fijubriju'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hulk_apps_chat.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'what1234ever'

    # Initialize
    socketio.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()  # Create database tables for our data models

    # Import and register Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Placeholder for chat blueprint registration
    # from .chat import chat_bp
    # app.register_blueprint(chat_bp)

    return app


# if __name__ == '__main__':
#     from hulk_apps_chat import create_app, socketio
#
#     app = create_app()
#     socketio.run(app, debug=True)
