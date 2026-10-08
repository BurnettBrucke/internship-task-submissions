import hashlib
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gateway_service.app.models.user import User


class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_bytes(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000,
        )

        return (
            salt.hex()
            + ":"
            + password_hash.hex()
        )

    @staticmethod
    def verify_password(
        password: str,
        stored_password: str,
    ) -> bool:
        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000,
        )

        return secrets.compare_digest(
            password_hash.hex(),
            hash_hex,
        )

    async def register_user(
        self,
        session: AsyncSession,
        username: str,
        password: str,
    ):
        result = await session.execute(
            select(User).where(User.username == username)
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            return None

        user = User(
            username=username,
            password_hash=self.hash_password(password),
            role="user",
        )

        session.add(user)

        await session.commit()
        await session.refresh(user)

        return {
            "id": str(user.id),
            "username": user.username,
            "role": user.role,
        }

    async def get_user(
        self,
        session: AsyncSession,
        username: str,
    ):
        result = await session.execute(
            select(User).where(User.username == username)
        )

        return result.scalar_one_or_none()

    async def verify_user(
        self,
        session: AsyncSession,
        username: str,
        password: str,
    ):
        user = await self.get_user(
            session,
            username,
        )

        if not user:
            return None

        if not self.verify_password(
            password,
            user.password_hash,
        ):
            return None

        return {
            "id": str(user.id),
            "username": user.username,
            "role": user.role,
        }


auth_service = AuthService()