from flask import request, jsonify
from . import chat_bp
from .. import db
from ..models import ChatRoom, User


@chat_bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    user_id = data.get('user_id')  # Assuming you're passing user ID for now; adjust based on your auth system

    if not name:
        return jsonify({'error': 'Room name is required'}), 400

    if ChatRoom.query.filter_by(name=name).first():
        return jsonify({'error': 'Room name already exists'}), 409

    new_room = ChatRoom(name=name, description=description, creator_id=user_id)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({'message': 'Room created successfully', 'room': {'name': name, 'description': description}}), 201


@chat_bp.route('/rooms', methods=['GET'])
def list_rooms():
    rooms = ChatRoom.query.all()
    return jsonify(
        {'rooms': [{'id': room.id, 'name': room.name, 'description': room.description} for room in rooms]}), 200
