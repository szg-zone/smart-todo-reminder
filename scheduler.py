import time
import asyncio
from datetime import datetime, timedelta
from flask import Flask
from config import Config
from models import db, Task, User
from telegram import Bot

# Initialize Flask + DB
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Telegram Bot setup
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)

async def send_telegram_message(chat_id, message):
    """Send a Telegram message in its own event loop (safe & reliable)."""
    try:
        # Each send gets a fresh loop to avoid 'Event loop closed' issues
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

                # Build datetime for task
                if task.time:
                    task_datetime = datetime.strptime(f"{task.date} {task.time}", "%Y-%m-%d %H:%M")
                else:
                    task_datetime = datetime.strptime(task.date, "%Y-%m-%d")

                # Send reminder 5 minutes before (you can change this)
                remind_time = task_datetime - timedelta(minutes=5)

                # If we’re within 5 minutes before or at task time
                if remind_time <= now <= task_datetime + timedelta(minutes=1):
                    message = (
                        f"🔔 *Reminder for {user.username}*\n\n"
                        f"📝 *{task.title}*\n"
                        f"📅 Date: `{task.date}`\n"
                        f"⏰ Time: `{task.time or 'Not specified'}`\n"
                        f"💬 {task.description or 'No details provided.'}"
                    )

                    # ✅ Run in isolated loop
                    asyncio.run(send_telegram_message(user.telegram_chat_id, message))

                    # Mark as notified
                    task.notified = True
                    db.session.commit()
                    print(f"✅ Reminder sent for task '{task.title}'")

            except Exception as e:
                print(f"⚠️ Error checking task '{task.title}': {e}")

def run_loop_forever():
    print("🚀 Scheduler run loop starting...")
    while True:
        check_and_send_reminders()
        time.sleep(60)
