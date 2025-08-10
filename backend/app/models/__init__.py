from .quiz import Quiz, Question, Option
from .lead import Lead
# backend/app/models/__init__.py
from app.db.base import Base  # re-export
from .tenant import Tenant    # чтобы Alembic видел таблицу tenants
