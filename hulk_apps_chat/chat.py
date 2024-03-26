import os
from time import time

from flask import Blueprint, request, session
from flask_socketio import join_room, leave_room, send, emit

from datetime import datetime
from . import socketio, db, redis_client
from .models import Message

chat_bp = Blueprint('chat', __name__)

# Rate limit settings: No more than 1 message every 5 seconds
RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', '5'))


def is_rate_limited(user_id):
    """
    Check if the user is rate limited based on the last message timestamp.
    Now using Redis for persistence.
    """
    key = f"user:{user_id}:last_message_time"
    last_message_time = redis_client.get(key)

    if last_message_time is not None:
        last_message_time = float(last_message_time)
        current_time = time()

        if (current_time - last_message_time) < RATE_LIMIT_SECONDS:
            return True

    # Update the last message timestamp for the user in Redis
    redis_client.set(key, str(current_time), ex=RATE_LIMIT_SECONDS)
    return False


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
    user_id = session.get('user_id')
    if not user_id:
        # Handle case where user_id is not in session
        emit('error', {'message': 'Authentication required.'}, room=request.sid)
        return

    if is_rate_limited(user_id):
        emit('rate_limit', {'message': 'You are sending messages too quickly. Please wait.'}, room=user_id)
        return

    username = data['username']
    room = data['room']
    message_text = data['message']
    timestamp = datetime.utcnow()

    message = Message(username=username, room=room, message=message_text, timestamp=timestamp)
    db.session.add(message)
    db.session.commit()

    emit('receive_message', data, room=room)
