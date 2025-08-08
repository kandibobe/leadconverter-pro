from celery import Celery

celery_app = Celery('leadconverter')

@celery_app.task(name='send_lead_notification')
def send_lead_notification(payload: dict, signature: str) -> None:
    """Send lead notification to Telegram bot."""
    # Implementation would send the payload to a bot using the signature.
    pass
