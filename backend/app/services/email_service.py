from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
from app.core.config import settings
from app.schemas import LeadOut

async def send_lead_confirmation_email(lead_data: LeadOut, pdf_path: str):
    """
    Асинхронно отправляет email с PDF-сметой клиенту через SendGrid.
    """
    message = Mail(
        from_email=settings.MAIL_FROM,
        to_emails=lead_data.client_email,
        subject=f"Ваша предварительная смета от {settings.PROJECT_NAME}",
        html_content="<strong>Здравствуйте!</strong><p>Спасибо за интерес к нашим услугам. Ваша смета прикреплена к этому письму.</p>"
    )

    with open(pdf_path, 'rb') as f:
        data = f.read()
    encoded_file = base64.b64encode(data).decode()

    attached_file = Attachment(
        FileContent(encoded_file),
        FileName(pdf_path.split('/')[-1]),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attached_file

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = await sg.send(message)
        print(f"Email отправлен на {lead_data.client_email}, статус: {response.status_code}")
    except Exception as e:
        print(f"Ошибка отправки email через SendGrid: {e}")