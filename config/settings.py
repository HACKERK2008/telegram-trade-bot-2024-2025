# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    ANGEL_CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
    ANGEL_MPIN = os.getenv("ANGEL_MPIN")
    ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
    TOTP_SECRET = os.getenv("TOTP_SECRET")
    ANGELONE_TRADING_API_KEY: str = os.getenv("ANGELONE_TRADING_API_KEY", "")
    ANGELONE_HISTORICAL_API_KEY: str = os.getenv("ANGELONE_HISTORICAL_API_KEY", "")

    LOCAL_IP = os.getenv("LOCAL_IP")
    PUBLIC_IP = os.getenv("PUBLIC_IP")
    MAC_ADDRESS = os.getenv("MAC_ADDRESS")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    SENTIMENT_API_KEY = os.getenv("SENTIMENT_API_KEY")
    OPTIONS_API_KEY = os.getenv("OPTIONS_API_KEY")

    ENVIRONMENT = os.getenv("ENVIRONMENT")
    LOG_LEVEL = os.getenv("LOG_LEVEL")

    SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "false").lower() == "true"
    SCHEDULER_INTERVAL_MINUTES = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "15"))

    ALERT_EMAIL = os.getenv("ALERT_EMAIL")
    ALERT_SMS_NUMBER = os.getenv("ALERT_SMS_NUMBER")

    AI_PROVIDER = os.getenv("AI_PROVIDER")
    AI_API_KEY = os.getenv("AI_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL")

    DATA_SOURCE = os.getenv("DATA_SOURCE")
    DATA_SOURCE_API_KEY = os.getenv("DATA_SOURCE_API_KEY")

    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE")
    MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "5"))

settings = Settings()
