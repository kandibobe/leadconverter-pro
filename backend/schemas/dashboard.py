from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_leads: int
    average_check: float
