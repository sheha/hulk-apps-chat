from dotenv import load_dotenv  # load env variables, .env used for development
from hulk_apps_chat import create_app

load_dotenv()

app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
