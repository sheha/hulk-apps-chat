from datetime import datetime

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    status = db.Column(db.String(50), default='sent')

    def __repr__(self):
        return f'<Message {self.message[:30]}>'


# Association table for room members
RoomMember = db.Table('room_member',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('room_id', db.Integer, db.ForeignKey('chat_room.id'), primary_key=True)
                      )


class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref='created_rooms')
    members = db.relationship('User', secondary=RoomMember, backref=db.backref('joined_rooms', lazy='dynamic'))

    def __repr__(self):
        return f'<ChatRoom {self.name}>'
