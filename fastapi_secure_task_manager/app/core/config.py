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


settings = Settings()