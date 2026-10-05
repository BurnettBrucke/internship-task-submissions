from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    processing_base_url: str
    processing_timeout_seconds: float
    gateway_service_token: str

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore