from app.schemas.lead import Lead

class NotificationService:
    def send_new_lead_notification(self, lead_data: Lead):
        """
        Сервис-заглушка для отправки уведомлений.
        В реальном приложении здесь будет логика отправки в Telegram, Email и т.д.
        """
        print("="*50)
        print("🚀 НОВЫЙ ЛИД ПОЛУЧЕН! 🚀")
        print(f"Email клиента: {lead_data.email}")
        print(f"Итоговая стоимость: {lead_data.final_price} RUB")
        print("Ответы клиента:")
        for key, value in lead_data.answers_data.items():
            print(f"  - {key}: {value}")
        print("="*50)

notification = NotificationService()