# backend/app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import quizzes, leads, dashboard # Добавили leads и dashboard
from app.api.v1.endpoints import quizzes, leads, dashboard, login, settings # <-- ДОБАВИЛИ login и settings

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])