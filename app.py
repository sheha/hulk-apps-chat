from dotenv import load_dotenv
load_dotenv()
from hulk_apps_chat import create_app, socketio
from hulk_apps_chat.models import User, Message

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
