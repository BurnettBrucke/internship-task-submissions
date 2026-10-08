from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    processing_base_url: str
    processing_timeout_seconds: float = 5.0
    processing_retry_count: int = 2
    processing_retry_delay_seconds: float = 0.2

    internal_service_token: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    
    database_url: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

settings = Settings()