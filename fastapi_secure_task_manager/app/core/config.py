import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "fastapi_secure_task_manager"
    )

    APP_ENV = os.getenv(
        "APP_ENV",
        "local"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"

    # Day 6 - JWT authentication settings
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "30"
        )
    )

    # Day 6 - password/login security settings
    PASSWORD_HASH_SCHEME = os.getenv(
        "PASSWORD_HASH_SCHEME",
        "argon2"
    )

    MAX_LOGIN_ATTEMPTS = int(
        os.getenv(
            "MAX_LOGIN_ATTEMPTS",
            "5"
        )
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    # Day 7 - PostgreSQL settings
    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    DB_POOL_SIZE = int(
        os.getenv(
            "DB_POOL_SIZE",
            "10"
        )
    )

    DB_MAX_OVERFLOW = int(
        os.getenv(
            "DB_MAX_OVERFLOW",
            "20"
        )
    )

    # Day 7 - Redis settings
    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    CACHE_TTL_SECONDS = int(
        os.getenv(
            "CACHE_TTL_SECONDS",
            "300"
        )
    )


settings = Settings()