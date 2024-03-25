from flask import Blueprint, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from . import socketio

chat_bp = Blueprint('chat', __name__)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


@socketio.on('message')
def handle_message(data):
    emit('receive_message', data, to=data['room'])
