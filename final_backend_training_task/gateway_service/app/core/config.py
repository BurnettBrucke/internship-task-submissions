from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    processing_base_url: str
    processing_timeout_seconds: float
    processing_service_token: str

    redis_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore