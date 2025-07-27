from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "LeadConverter Pro"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # Mail settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()