from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Зависимость (dependency), которая предоставляет сессию базы данных для одного запроса.
    Гарантирует, что сессия будет закрыта после выполнения запроса.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
