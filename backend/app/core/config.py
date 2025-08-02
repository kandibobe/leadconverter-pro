# ... (предыдущие настройки) ...
class Settings(BaseSettings):
    # ...
    # Mail settings
    MAIL_FROM: str
    SENDGRID_API_KEY: str

    # Telegram settings
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()