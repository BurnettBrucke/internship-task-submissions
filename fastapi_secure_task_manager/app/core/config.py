from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "fastapi_secure_task_manager"
    APP_ENV: str = "local"
    DEBUG: bool = True

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PASSWORD_HASH_SCHEME: str = "argon2"
    MAX_LOGIN_ATTEMPTS: int = 5
    LOG_LEVEL: str = "INFO"
    
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()