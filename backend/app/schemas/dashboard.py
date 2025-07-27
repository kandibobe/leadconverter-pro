from pydantic import BaseModel

class DashboardMetrics(BaseModel):
    """
    Схема для отображения ключевых метрик на дашборде.
    Соответствует FR-6 из ТЗ.
    """
    quiz_views: int = 0
    calculations_started: int = 0
    leads_count: int
    average_check: float