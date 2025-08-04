from pydantic import BaseModel, Field


class DashboardMetrics(BaseModel):
    """Schema representing metrics displayed on the admin dashboard."""
    total_leads: int = Field(..., description="Общее количество лидов")
    average_check: float = Field(..., description="Средний чек по лидам")
