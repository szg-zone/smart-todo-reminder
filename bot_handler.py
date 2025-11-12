# bot_handler.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from models import db, User
from flask import Flask

# ---------------------------
# 1️⃣ Load Flask app context for DB access
# ---------------------------
flask_app = Flask(__name__)
flask_app.config.from_object("config.Config")
db.init_app(flask_app)

# ---------------------------
# 2️⃣ Load Telegram token from environment
# ---------------------------
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Missing TELEGRAM_BOT_TOKEN in environment")

# ---------------------------
# 3️⃣ Build Telegram Application
# ---------------------------
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()


# ---------------------------
# 4️⃣ Command handler: /start
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command with user ID (payload)."""
    if context.args:  # /start <user_id>
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


# ---------------------------
# 5️⃣ Add command handler to bot
# ---------------------------
bot_app.add_handler(CommandHandler("start", start))


# ---------------------------
# 6️⃣ Run bot directly (for testing only)
# ---------------------------
if __name__ == "__main__":
    print("🤖 Telegram bot is running... (Press CTRL+C to stop)")
    bot_app.run_polling()
