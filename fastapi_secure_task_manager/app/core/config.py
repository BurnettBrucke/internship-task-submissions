from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    #Application
    app_name: str = "fastapi_secure_task_manager"
    app_env: str = "local"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 300

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # Password security
    password_hash_scheme: str = "argon2"

    # Login protection
    max_login_attempts: int = 5

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )
    max_login_attempts :int = 5
    block_duration_minutes :int = 15


settings = Settings() # type: ignore