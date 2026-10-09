from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "task-management-api"
    APP_ENV: str = "local"
    DEBUG: bool = True

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PASSWORD_HASH_SCHEME: str = "argon2"
    MAX_LOGIN_ATTEMPTS: int = 5

    DATABASE_URL: str

    REDIS_URL: str = "redis://localhost:6379/0"

    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    CACHE_TTL_SECONDS: int = 300

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()