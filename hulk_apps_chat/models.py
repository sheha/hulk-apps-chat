from datetime import datetime

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    room = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for group messages
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    status = db.Column(db.String(50), default='sent')

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    creator = db.relationship('User', foreign_keys=[creator_id])

    def __repr__(self):
        return f'<ChatRoom {self.name}>'