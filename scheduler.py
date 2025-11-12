import time
import asyncio
from datetime import datetime, timedelta
from flask import Flask
from models import db, Task, User
from telegram import Bot
import os

# ---------------------------
# 1️⃣ Load token from environment
# ---------------------------
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Missing TELEGRAM_BOT_TOKEN in environment")

# ---------------------------
# 2️⃣ Flask app + DB
# ---------------------------
app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

# ---------------------------
# 3️⃣ Telegram bot
# ---------------------------
bot = Bot(token=BOT_TOKEN)

# ---------------------------
# 4️⃣ Send message function
# ---------------------------
async def send_telegram_message(chat_id, message):
    """Send a Telegram message asynchronously (safe for each loop)."""
    try:
        # Create and use a fresh event loop per message
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        print(f"✅ Sent Telegram message to {chat_id}")
    except Exception as e:
        print(f"❌ Failed to send message to {chat_id}: {e}")
    finally:
        try:
            new_loop.close()
        except:
            pass

# ---------------------------
# 5️⃣ Reminder checker
# ---------------------------
def check_and_send_reminders():
    """Check all users' tasks and send Telegram reminders if due."""
    with app.app_context():
        now = datetime.now()
        tasks = Task.query.filter_by(notified=False).all()

        for task in tasks:
            try:
                user = db.session.get(User, task.user_id)
                if not user or not user.telegram_chat_id:
                    continue

                # Construct datetime
                if task.time:
                    task_datetime = datetime.strptime(f"{task.date} {task.time}", "%Y-%m-%d %H:%M")
                else:
                    task_datetime = datetime.strptime(task.date, "%Y-%m-%d")

                remind_time = task_datetime - timedelta(minutes=5)

                # Within reminder window
                if remind_time <= now <= task_datetime + timedelta(minutes=1):
                    message = (
                        f"🔔 *Reminder for {user.username}*\n\n"
                        f"📝 *{task.title}*\n"
                        f"📅 Date: `{task.date}`\n"
                        f"⏰ Time: `{task.time or 'Not specified'}`\n"
                        f"💬 {task.description or 'No details provided.'}"
                    )

                    # Send message
                    asyncio.run(send_telegram_message(user.telegram_chat_id, message))

                    task.notified = True
                    db.session.commit()
                    print(f"✅ Reminder sent for task '{task.title}'")

            except Exception as e:
                print(f"⚠️ Error checking task '{task.title}': {e}")

# ---------------------------
# 6️⃣ Loop runner (called from main.py)
# ---------------------------
def run_loop_forever():
    print("🚀 Scheduler run loop starting...")
    while True:
        check_and_send_reminders()
        time.sleep(60)
