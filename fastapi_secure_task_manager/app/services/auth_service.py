# ============================================================
# 1. IMPORTS
# ============================================================
from app.core.config import settings
from app.data.store import users_db, login_attempts
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
# MAX_LOGIN_ATTEMPTS = 5

# ============================================================
# 2. REGISTER USER
# ============================================================

def register_user(user: UserCreate) -> dict:
    """
    Register a new user.

    Steps:
    1. Check whether username already exists.
    2. Hash the password.
    3. Store user information.
    4. Never store the plain-text password.
    """

    # --------------------------------------------------------
    # Check duplicate username
    # --------------------------------------------------------
    if user.username in users_db:
        raise ValueError("Username already exists")

    # --------------------------------------------------------
    # Hash password
    # --------------------------------------------------------
    password_hash = hash_password(user.password)

    # --------------------------------------------------------
    # Store user
    # --------------------------------------------------------
    user_data = {
        "username": user.username,
        "email": str(user.email),
        "password_hash": password_hash,
        "role": user.role.value,
    }

    users_db[user.username] = user_data

    # --------------------------------------------------------
    # Return safe user information
    # --------------------------------------------------------
    return {
        "username": user_data["username"],
        "email": user_data["email"],
        "role": user_data["role"],
    }

# ============================================================
# 3. LOGIN USER
# ============================================================

def login_user(username: str, password: str) -> dict:
    user = users_db.get(username)

    # Check whether the account has reached the maximum failed attempts
    if login_attempts.get(username, 0) >= settings.MAX_LOGIN_ATTEMPTS:
        raise ValueError(
            "Too many failed login attempts. Please try again later."
        )

    # User does not exist
    if user is None:
        login_attempts[username] = login_attempts.get(username, 0) + 1

        raise ValueError("Invalid username or password")

    # Password is incorrect
    if not verify_password(password, user["password_hash"]):
        login_attempts[username] = login_attempts.get(username, 0) + 1

        raise ValueError("Invalid username or password")

    # Successful login → reset failed attempts
    login_attempts[username] = 0

    access_token = create_access_token(
        username=user["username"],
        role=user["role"],
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,
    }