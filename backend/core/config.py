POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", ""),
POSTGRES_SERVER=os.getenv("POSTGRES_SERVER", ""),
POSTGRES_DB=os.getenv("POSTGRES_DB", ""),
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

    class Config:
        case_sensitive = True

settings = Settings()