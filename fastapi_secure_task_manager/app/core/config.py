# ============================================================
# 1. IMPORT REQUIRED CLASS
# ============================================================

from pydantic_settings import BaseSettings, SettingsConfigDict


# ============================================================
# 2. APPLICATION SETTINGS CLASS
# ============================================================

class Settings(BaseSettings):
    """
    Application configuration.
    Values are loaded from the .env file.
    """

    # --------------------------------------------------------
    # Application settings
    # --------------------------------------------------------

    APP_NAME: str = "fastapi_secure_task_manager"
    APP_ENV: str = "local"
    DEBUG: bool = True

    # --------------------------------------------------------
    # Database settings
    # --------------------------------------------------------

    DATABASE_URL: str
    TEST_DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # --------------------------------------------------------
    # Redis / Cache settings
    # --------------------------------------------------------

    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 300

    # --------------------------------------------------------
    # JWT settings
    # --------------------------------------------------------

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --------------------------------------------------------
    # Security settings
    # --------------------------------------------------------

    PASSWORD_HASH_SCHEME: str = "argon2"
    MAX_LOGIN_ATTEMPTS: int = 5

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    LOG_LEVEL: str = "INFO"

    # --------------------------------------------------------
    # Tell Pydantic where configuration comes from
    # --------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# ============================================================
# 3. CREATE SETTINGS OBJECT
# ============================================================

settings = Settings()