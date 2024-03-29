from flask import request, session
from flask_jwt_extended import decode_token
from flask_socketio import join_room, leave_room, send, emit

from datetime import datetime
from hulk_apps_chat import socketio, db, redis_client
from ..models import Message, User
from hulk_apps_chat.utils import set_user_session, get_user_id, remove_user_session, is_rate_limited


@socketio.on('join')
def on_join(data):
    user_id = session.get('user_id')
    if user_id:
        room_id = data['room']
        join_room(room_id)
        username = User.query.get(user_id).username
        # Fetch the last 20 messages from this room
        recent_messages = Message.query.filter_by(room_id=room_id).order_by(Message.timestamp.desc()).limit(20).all()
        for message in recent_messages[::-1]:  # Reverse to send in chronological order
            emit('message', {
                'username': message.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }, room=room_id)

        send(username + ' has entered the room.', room=room_id)


@socketio.on('leave')
def on_leave(data):
    # Retrieve user ID from Flask session
    user_id = session.get('user_id')
    if user_id is None:
        # Handle the case where the user ID is not found in the session
        emit('error', {'message': 'Authentication required.'}, room=request.sid)
        return

    # Query the database for the user by user_id to get the username
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        # Handle the case where the user does not exist in the database
        emit('error', {'message': 'User not found.'}, room=request.sid)
        return

    # Use the room ID from the data passed by the client
    room_id = data.get('room')
    if room_id:
        leave_room(room_id)
        send(f"{user.username} has left the room.", room=room_id)
    else:
        # Handle the case where room_id is not provided
        emit('error', {'message': 'Room ID required.'}, room=request.sid)


@socketio.on('message')
def handle_message(data):
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if not user_id:
        # Handle case where user_id is not in session
        emit('error', {'message': 'Authentication required.'}, room=request.sid)
        return

    if is_rate_limited(user_id):
        emit('rate_limit', {'message': 'You are sending messages too quickly. Please wait.'}, room=user_id)
        return

    username = user.username
    room_id = data['room']
    message_text = data['message']
    timestamp = datetime.utcnow()
    recipient_id = data.get('recipient_id', None)

    if recipient_id:
        # This is a private message
        message = Message(username=username, room_id=room_id, recipient_id=recipient_id, message=message_text,
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
        message = Message(username=username, room_id=room_id, message=message_text, timestamp=timestamp)
        # Emit to the room for public messages
        emit('receive_message', {
            'username': username,
            'message': message_text,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, room=room_id)

    db.session.add(message)
    db.session.commit()


@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    try:
        # Attempt to decode the token
        decoded_token = decode_token(token)

        user_id = decoded_token['sub']['user_id']

        session_id = request.sid
        set_user_session(user_id, session_id)

        session['user_id'] = user_id

        redis_client.set(f'user_online:{user_id}', 'online')
        emit('user_online', {'user_id': user_id, 'online': True}, broadcast=True)

    except Exception as e:
        print(f'Connection failed: {e}')
        emit('error', {'message': 'Authentication failed'}, room=request.sid)
        return False


@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    user_id = get_user_id(session_id)
    if user_id:
        remove_user_session(user_id, session_id)

        redis_client.delete(f'user_online:{user_id}')
        # Emit an event to update the user's online status
        emit('user_online', {'user_id': user_id, 'online': False}, broadcast=True)


@socketio.on('message_delivered')
def on_message_delivered(data):
    message_id = data['message_id']
    message = Message.query.get(message_id)
    if message:
        message.status = 'delivered'
        db.session.commit()
        emit('update_message_status', {'message_id': message_id, 'status': 'delivered'}, room=message.room)


@socketio.on('message_read')
def on_message_read(data):
    message_id = data['message_id']
    message = Message.query.get(message_id)
    if message:
        message.status = 'read'
        db.session.commit()
        emit('update_message_status', {'message_id': message_id, 'status': 'read'}, room=message.room)
