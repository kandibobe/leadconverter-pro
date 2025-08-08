import logging
import os

from fastapi import APIRouter

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", status_code=200)
def check_health():
    """Простой эндпоинт для проверки работоспособности сервиса."""
    logger.debug("Health check requested")
    return {"status": "ok"}
