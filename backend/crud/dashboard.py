from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.schemas.dashboard import DashboardMetrics


def get_dashboard_metrics(db: Session) -> DashboardMetrics:
    """Calculate basic statistics for the dashboard."""
    total_leads = db.query(func.count(Lead.id)).scalar() or 0
    average_check = db.query(func.avg(Lead.final_price)).scalar() or 0.0
    return DashboardMetrics(total_leads=total_leads, average_check=average_check)
