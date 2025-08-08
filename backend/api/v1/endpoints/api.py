# backend/app/api/v1/api.py
import logging
import os

from fastapi import APIRouter
from app.api.v1.endpoints import quizzes, leads, dashboard  # Добавили leads и dashboard


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])  # Новая строка
api_router.include_router(
    dashboard.router, prefix="/dashboard", tags=["dashboard"]
)  