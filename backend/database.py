import os
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/leadconverter"
)

# Включаем поддержку RLS на уровне соединения
engine = create_engine(
    DATABASE_URL, connect_args={"options": "-c row_security=on"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db(tenant_id: str) -> Generator:
    """Возвращает сессию БД с установленным tenant_id."""
    db = SessionLocal()
    db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": tenant_id})
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Создание таблиц и настройка политик RLS."""
    Base.metadata.create_all(bind=engine)
    tables = ["leads", "quizzes", "questions", "options"]
    with engine.begin() as conn:
        for table in tables:
            conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
            conn.execute(text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))
            conn.execute(text(f"DROP POLICY IF EXISTS tenant_isolation ON {table}"))
            conn.execute(
                text(
                    f"""
                    CREATE POLICY tenant_isolation ON {table}
                    USING (tenant_id = current_setting('app.tenant_id')::text)
                    WITH CHECK (tenant_id = current_setting('app.tenant_id')::text)
                    """
                )
            )


