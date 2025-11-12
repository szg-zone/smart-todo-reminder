import os

class Config:
    SECRET_KEY = '6e03ca4176a87e08a8a957bb797006f9'  # can be any random string
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Telegram Bot Config (we'll fill these later)
    TELEGRAM_BOT_TOKEN = '8598712050:AAFj_7GaoUPeV1ZrYo3QrEooCfOtnLndxmo'
    TELEGRAM_CHAT_ID = '8444949634'
