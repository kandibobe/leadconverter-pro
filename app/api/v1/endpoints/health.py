from fastapi import APIRouter

router = APIRouter()

@router.get("/health", status_code=200)
def check_health():
    """
    Простой эндпоинт для проверки работоспособности сервиса.
    """
    return {"status": "ok"}