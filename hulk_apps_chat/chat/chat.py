from flask import request, session
from flask_socketio import join_room, leave_room, send, emit

from datetime import datetime
from hulk_apps_chat import socketio, db, redis_client
from ..models import Message
from hulk_apps_chat.utils import set_user_session, get_user_id, remove_user_session, is_rate_limited


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
    recipient_id = data.get('recipient_id', None)

    if recipient_id:
        # This is a private message
        message = Message(username=username, room=room, recipient_id=recipient_id, message=message_text,
                          timestamp=timestamp)
        # Emit to the specific recipient if it's a private message
        emit('receive_message', {
            'username': username,
            'message': message_text,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'recipient_id': recipient_id  # Include this to let the client know it's a private message
        }, room=recipient_id)
    else:
        # This is a public message
        message = Message(username=username, room=room, message=message_text, timestamp=timestamp)
        # Emit to the room for public messages
        emit('receive_message', {
            'username': username,
            'message': message_text,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, room=room)

    db.session.add(message)
    db.session.commit()


@socketio.on('connect')
def handle_connect():
    user_id = session.get('user_id')
    if user_id:
        session_id = request.sid
        set_user_session(user_id, session_id)

        redis_client.set(f'user_online:{user_id}', 'online')
        # Emit an event to update the user's online status
        emit('user_online', {'user_id': user_id, 'online': True}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    user_id = get_user_id(session_id)
    if user_id:
        remove_user_session(user_id, session_id)

        redis_client.delete(f'user_online:{user_id}')
        # Emit an event to update the user's online status
        emit('user_online', {'user_id': user_id, 'online': False}, broadcast=True)
