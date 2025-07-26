from pydantic_settings import BaseSettings
import os

# Загружаем переменные из .env файла, если он есть
from dotenv import load_dotenv
load_dotenv()

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

    class Config:
        case_sensitive = True

settings = Settings()