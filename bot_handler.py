from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import Config
from models import db, User
from flask import Flask

# Initialize Flask app context for database access
flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db.init_app(flask_app)

# Initialize Telegram Bot application
bot_app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

# ----------- START COMMAND HANDLER -----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command with user ID (payload)."""
    if context.args:  # Means there's a user ID after /start
        user_id = context.args[0]
        chat_id = update.effective_chat.id

        with flask_app.app_context():
            user = User.query.get(int(user_id))
            if user:
                user.telegram_chat_id = str(chat_id)
                db.session.commit()
                await update.message.reply_text(
                    f"✅ Hi {user.username}! Your Telegram account has been linked successfully.\n"
                    f"You’ll now receive reminders here 🔔."
                )
                print(f"Linked Telegram chat_id={chat_id} to user_id={user_id}")
            else:
                await update.message.reply_text("❌ Invalid link. Please log in again on the website.")
    else:
        await update.message.reply_text("👋 Hello! Please use the link from the website to link your account.")

# Add command handler
bot_app.add_handler(CommandHandler("start", start))

# ----------- RUN THE BOT -----------
if __name__ == "__main__":
    print("🤖 Telegram bot is running... (Press CTRL+C to stop)")
    bot_app.run_polling()
