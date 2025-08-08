from fastapi import APIRouter

from app.api.v1.endpoints import estimate, leads, quizzes, stripe_webhooks

api_router = APIRouter()
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(estimate.router, prefix="/estimate", tags=["estimate"])
api_router.include_router(stripe_webhooks.router, prefix="/stripe", tags=["stripe"])
