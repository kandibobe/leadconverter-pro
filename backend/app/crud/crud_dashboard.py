from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.lead import Lead
from app.schemas.dashboard import DashboardMetrics

def get_dashboard_metrics(db: Session) -> DashboardMetrics:
    """
    Рассчитывает ключевые метрики для дашборда.
    """
    # Считаем количество лидов
    leads_count = db.query(Lead).count()

    # Считаем средний чек
    # func.avg(Lead.final_price) возвращает среднее значение по колонке
    average_check_query = db.query(func.avg(Lead.final_price)).scalar()
    # Если лидов нет, средний чек будет None, поэтому ставим 0.0
    average_check = average_check_query if average_check_query is not None else 0.0

    # TODO: В будущем добавить логику для подсчета просмотров и начатых расчетов
    # Это потребует сохранения событий в БД.
    
    metrics = DashboardMetrics(
        leads_count=leads_count,
        average_check=round(average_check, 2) # Округляем до 2 знаков
    )
    
    return metrics

# Создаем экземпляр для импорта
dashboard = get_dashboard_metrics