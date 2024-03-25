from flask import Blueprint, request
from flask_socketio import join_room, leave_room, send, emit
from datetime import datetime

from . import socketio, db
from .models import Message

chat_bp = Blueprint('chat', __name__)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    # Fetch the last 20 messages from this room
    recent_messages = Message.query.filter_by(room=room).order_by(Message.timestamp.desc()).limit(20).all()
    for message in recent_messages[::-1]:  # Reverse to send in chronological order
        emit('message', {
            'username': message.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, room=room)

    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message_text = data['message']
    timestamp = datetime.utcnow()

    # Save the message to the database
    message = Message(username=username, room=room, message=message_text, timestamp=timestamp)
    db.session.add(message)
    db.session.commit()

    emit('receive_message', data, room=room)
