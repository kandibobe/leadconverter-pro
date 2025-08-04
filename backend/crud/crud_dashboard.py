from sqlalchemy.orm import Session


def get_dashboard_metrics(db: Session) -> dict:
    """Return basic metrics for the dashboard.

    Currently returns static values as a placeholder.
    """
    return {"total_leads": 0, "average_check": 0.0}
