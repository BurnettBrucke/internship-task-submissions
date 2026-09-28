from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.data.store import (
    add_user,
    clear_login_security,
    get_blocked_until,
    get_login_attempts,
    get_user,
    set_blocked_until,
    set_login_attempts,
)


def register_user(username: str, email: str, password: str, role: str):
    if get_user(username):
        return None

    user = {
        "username": username,
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
    }

    add_user(user)
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)

    if not user:
        return None

    now = datetime.now(timezone.utc)
    blocked_until = get_blocked_until(username)

    # Check temporary block
    if blocked_until and now < blocked_until:
        return "blocked"

    # Block period has expired
    if blocked_until and now >= blocked_until:
        clear_login_security(username)

    failed_attempts = get_login_attempts(username)

    # Check password
    if not verify_password(password, user["password_hash"]):
        failed_attempts += 1
        set_login_attempts(username, failed_attempts)

        # Block for 5 minutes after maximum attempts
        if failed_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            blocked_until = now + timedelta(minutes=5)
            set_blocked_until(username, blocked_until)
            return "blocked"

        return None

    # Successful login resets security counters
    clear_login_security(username)

    return user


def create_user_token(user: dict):
    return create_access_token(
        username=user["username"],
        role=user["role"],
    )