from typing import Generator
from fastapi import Header, Depends

from app.database import get_db as db_session

def get_tenant_id(x_tenant_id: str = Header(...)) -> str:
    """Получить идентификатор арендатора из заголовка."""
    return x_tenant_id


def get_db(tenant_id: str = Depends(get_tenant_id)) -> Generator:
    """Предоставляет сессию БД для указанного tenant_id."""
    yield from db_session(tenant_id)
