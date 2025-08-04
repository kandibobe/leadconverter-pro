# backend/app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import quizzes, leads, dashboard # Добавили leads и dashboard

api_router = APIRouter()
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"]) # Новая строка
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"]) # Новая строка