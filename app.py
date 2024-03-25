from dotenv import load_dotenv
from hulk_apps_chat import create_app, socketio

load_dotenv()  # Take environment variables from .env for development environment

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
