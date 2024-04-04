from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import chat_bp
from .. import db
from ..models import ChatRoom, User, Message
from ..utils import is_valid_room_name


@chat_bp.route('/rooms', methods=['POST'])
@jwt_required()  # Require access token for this route
def create_room():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    user_identity = get_jwt_identity()
    user_id = user_identity['user_id'] if 'user_id' in user_identity else None

    if not user_id:
        return jsonify({'error': 'Invalid user ID'}), 400

    if not name:
        return jsonify({'error': 'Room name is required'}), 400

    if ChatRoom.query.filter_by(name=name).first():
        return jsonify({'error': 'Room name already exists'}), 409

    if not is_valid_room_name(name):
        return jsonify({'error': 'Invalid room name'}), 400

    new_room = ChatRoom(name=name, description=description, creator_id=user_id)

    db.session.add(new_room)
    db.session.commit()

    return jsonify({'message': 'Room created successfully',
                    'room': {'id': new_room.id, 'name': name, 'description': description}}), 201


@chat_bp.route('/rooms', methods=['GET'])
def list_rooms():
    rooms = ChatRoom.query.all()
    room_list = []
    for room in rooms:
        room_info = {
            'id': room.id,
            'name': room.name,
            'description': room.description,
            'creator': room.creator.username if room.creator else 'Unknown'
        }
        room_list.append(room_info)
    return jsonify({'rooms': room_list}), 200


@chat_bp.route('/rooms/join', methods=['POST'])
@jwt_required()
def join_room():
    room_id = request.json.get('room_id')
    user_id = get_jwt_identity()

    room = ChatRoom.query.get(room_id)
    user = User.query.get(user_id)

    if not room or not user:
        return jsonify({"message": "Room or User not found"}), 404

    if user not in room.members:
        room.members.append(user)
        db.session.commit()

    return jsonify({"message": "User added to room"}), 200


@chat_bp.route('/rooms/<int:room_id>/members', methods=['GET'])
def list_room_members(room_id):
    room = ChatRoom.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found"}), 404

    members = []
    for user in room.members:
        members.append({
            'id': user.id,
            'username': user.username,
            'isCreator': user.id == room.creator_id
        })
    print(members)
    return jsonify({"members": members}), 200


@chat_bp.route('/rooms/<int:room_id>/remove_member', methods=['POST'])
@jwt_required()
def remove_member(room_id):
    data = request.get_json()
    user_id_to_remove = data.get('user_id')
    user_id_requesting = get_jwt_identity()

    room = ChatRoom.query.get(room_id)
    if room.creator_id != user_id_requesting:
        return jsonify({"message": "Only the room creator can remove members"}), 403

    user_to_remove = User.query.get(user_id_to_remove)
    if user_to_remove and user_to_remove in room.members:
        room.members.remove(user_to_remove)
        db.session.commit()
        return jsonify({"message": "User removed from room"}), 200
    else:
        return jsonify({"message": "User not in room"}), 404


@chat_bp.route('/rooms/<int:room_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(room_id):
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.timestamp.asc()).all()
    messages_json = [{
        'id': message.id,
        'username': message.username,
        'message': message.message,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'status': message.status
    } for message in messages]

    return jsonify({'messages': messages_json}), 200