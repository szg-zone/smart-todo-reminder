import os

class Config:
    # -----------------------------
    # Flask Settings
    # -----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")  # fallback for local dev

    # -----------------------------
    # Database Configuration
    # -----------------------------
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # Telegram Configuration
    # -----------------------------
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # loaded from .env
