from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем "движок" SQLAlchemy для подключения к БД.
# URL для подключения берется из наших настроек (которые, в свою очередь, из .env файла).
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Создаем фабрику сессий. Каждая сессия - это одно "общение" с базой данных.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)