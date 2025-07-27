from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from app.core.config import settings
from app.schemas import LeadOut

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / '../templates/email',
)

fm = FastMail(conf)

async def send_lead_confirmation_email(lead_data: LeadOut, pdf_path: str):
    """
    Асинхронно отправляет email с PDF-сметой клиенту.
    """
    message = MessageSchema(
        subject=f"Ваша предварительная смета от {settings.PROJECT_NAME}",
        recipients=[lead_data.client_email],
        body=f"Здравствуйте! Спасибо за интерес к нашим услугам. Ваша смета прикреплена к этому письму.",
        attachments=[pdf_path]
    )
    try:
        await fm.send_message(message)
        print(f"Email успешно отправлен на {lead_data.client_email}")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")