import os
from time import time

from . import redis_client

RATE_LIMIT_SECONDS = int(os.getenv('RATE_LIMIT_SECONDS', '5'))


# CHAT RATE LIMITER
def is_rate_limited(user_id):
    """
    Check if the user is rate limited based on the last message timestamp.
    Using Redis for persistence
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


# USER ONLINE STATUS
# storing the user - session mappings in redis
def is_user_online(user_id):
    return redis_client.exists(f'user_online:{user_id}')


def set_user_session(user_id, session_id):
    redis_client.set(f"user_session:{user_id}", session_id)
    redis_client.set(f"session_user:{session_id}", user_id)


def get_session_id(user_id):
    return redis_client.get(f"user_session:{user_id}")


def get_user_id(session_id):
    return redis_client.get(f"session_user:{session_id}")


def remove_user_session(user_id, session_id):
    redis_client.delete(f"user_session:{user_id}")
    redis_client.delete(f"session_user:{session_id}")

#CHAT ROOM validation
import re

def is_valid_room_name(name):
    """Define room name validation logic here."""
    return re.match(r'^\w+$', name)  # Example: Alphanumeric characters only
