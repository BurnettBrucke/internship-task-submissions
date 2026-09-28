from app.core.security import hash_password , verify_password
from app.data.store import users
from datetime import datetime, timedelta, timezone

from app.core.security import hash_password, verify_password
from app.data.store import users


MAX_LOGIN_ATTEMPTS = 5
BLOCK_DURATION_MINUTES = 15

login_attempts = {}
def find_user_by_username(username:str):
    for user in users.values():
        if user["username"] == username:
            return user

    return None

def find_user_by_id(user_id: int):
    return users.get(user_id)


def create_user(username : str , email : str , password : str , role : str):
    global users
    user_id = max(users.keys() , default= 0)+1

    user={
        "id" : user_id,
        "username": username,
        "email" :email,
        "password_hash" : hash_password(password),
        "role":role
    }

    users[user_id] = user

    return user

def authenticate_user(username : str , password : str,):
    user = find_user_by_username(username)

    if not user:
        return None
    if not verify_password(password , user["password_hash"],):
        return None

    return user

def is_login_blocked(username: str) -> bool:
    attempt_data = login_attempts.get(username)

    if not attempt_data:
        return False

    blocked_until = attempt_data.get("blocked_until")

    if blocked_until is None:
        return False

    if datetime.now(timezone.utc) < blocked_until:
        return True

    # Block expired, reset attempts
    login_attempts.pop(username, None)

    return False


def record_failed_login(username: str):
    attempt_data = login_attempts.get(
        username,
        {
            "count": 0,
            "blocked_until": None,
        },
    )

    attempt_data["count"] += 1

    if attempt_data["count"] >= MAX_LOGIN_ATTEMPTS:
        attempt_data["blocked_until"] = (
            datetime.now(timezone.utc)
            + timedelta(minutes=BLOCK_DURATION_MINUTES)
        )

    login_attempts[username] = attempt_data


def reset_login_attempts(username: str):
    login_attempts.pop(username, None)