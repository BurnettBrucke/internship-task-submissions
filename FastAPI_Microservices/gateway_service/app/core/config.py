from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Gateway -> Processing Service
    processing_base_url: str
    processing_timeout_seconds: int = 5

    # Service-to-service authentication
    gateway_service_client_id: str
    gateway_service_client_secret: str

    # JWT
    jwt_secret_key: str

    # Redis
    redis_url: str

    # PostgreSQL
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()