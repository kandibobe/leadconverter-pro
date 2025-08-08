"""Application configuration and environment helpers."""

import os
from pydantic_settings import BaseSettings


# Build a default DATABASE_URL for convenience.  The variables are retrieved only
# once at import time so repeated imports do not continually hit ``os.getenv``.
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")

raw_db_url = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    if POSTGRES_SERVER
    else ""
)
os.environ["DATABASE_URL"] = raw_db_url

class Settings(BaseSettings):
    """
    Класс для хранения всех настроек приложения.
    Настройки загружаются из переменных окружения.
    """
    PROJECT_NAME: str = "LeadConverter Pro"
    API_V1_STR: str = "/api/v1"

    # Настройки базы данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = [origin.strip() for origin in os.getenv("BACKEND_CORS_ORIGINS", "*").split(",") if origin]

    # Настройки безопасности
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # gRPC certificate paths
    GRPC_CERT_PATH: str | None = None
    GRPC_KEY_PATH: str | None = None
    GRPC_CA_PATH: str | None = None

    # API keys
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    LOG_SUMMARY_API_KEY: str | None = os.getenv("LOG_SUMMARY_API_KEY")

    class Config:
        case_sensitive = True
settings = Settings()