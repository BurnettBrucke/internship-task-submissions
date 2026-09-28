from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.data.store import users
from app.schemas.user import UserCreate


def get_user_by_username(username: str):
    for user in users:
        if user["username"] == username:
            return user

    return None


def get_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    return None


def create_user(user_data: UserCreate):
    if get_user_by_username(user_data.username):
        return None

    new_id = (
        max(user["id"] for user in users) + 1
        if users
        else 1
    )

    new_user = {
        "id": new_id,
        "username": user_data.username,
        "email": str(user_data.email),
        "password_hash": hash_password(user_data.password),
        "role": user_data.role,
    }

    users.append(new_user)

    return new_user


def authenticate_user(
    username: str,
    password: str
):
    user = get_user_by_username(username)

    if user is None:
        return None

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    return user


def generate_token(user: dict) -> str:
    return create_access_token(
        user_id=user["id"],
        username=user["username"],
        role=user["role"],
    )