import httpx
from app.core.config import settings
from app.schemas import LeadOut

async def send_telegram_notification(lead_data: LeadOut):
    """
    Асинхронно отправляет уведомление о новом лиде в Telegram.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    price_formatted = f"{lead_data.final_price:,.2f} RUB"
    
    text = (
        f"🚀 **Новый лид!**\n\n"
        f"**Email клиента:** {lead_data.client_email}\n"
        f"**Итоговая стоимость:** {price_formatted}\n\n"
        f"**Детали:**\n"
    )
    for question, answer in lead_data.answers_details.items():
        text += f"- *{question}*: {answer}\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=params)
            if response.status_code == 200:
                print(f"Уведомление в Telegram успешно отправлено в чат {chat_id}")
            else:
                print(f"Ошибка отправки в Telegram: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Исключение при отправке в Telegram: {e}")