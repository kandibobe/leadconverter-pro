"""Main API router aggregating individual endpoint routers."""

from fastapi import APIRouter
from app.api.v1.endpoints import dashboard, estimate, leads, quizzes

api_router = APIRouter()
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(estimate.router, prefix="/estimate", tags=["estimate"])
