from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.lead import Lead
from app.models.quiz import Quiz # <-- ИМПОРТИРУЕМ МОДЕЛЬ КВИЗА
from app.schemas.dashboard import DashboardMetrics

def get_dashboard_metrics(db: Session) -> DashboardMetrics:
    """
    Рассчитывает ключевые метрики для дашборда.
    """
    # Считаем количество лидов
    leads_count = db.query(Lead).count()

    # Считаем средний чек
    average_check_query = db.query(func.avg(Lead.final_price)).scalar()
    average_check = average_check_query if average_check_query is not None else 0.0

    # --- НОВАЯ ЛОГИКА: СЧИТАЕМ ПРОСМОТРЫ И СТАРТЫ ---
    # Суммируем просмотры и старты по всем квизам
    total_views_query = db.query(func.sum(Quiz.views)).scalar()
    total_starts_query = db.query(func.sum(Quiz.starts)).scalar()
    
    total_views = total_views_query if total_views_query is not None else 0
    total_starts = total_starts_query if total_starts_query is not None else 0
    # ------------------------------------------------

    metrics = DashboardMetrics(
        leads_count=leads_count,
        average_check=round(average_check, 2),
        quiz_views=total_views, # <-- ПЕРЕДАЕМ В СХЕМУ
        calculations_started=total_starts # <-- ПЕРЕДАЕМ В СХЕМУ
    )
    
    return metrics

dashboard = get_dashboard_metrics