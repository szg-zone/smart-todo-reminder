# main.py
import multiprocessing
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import components
from app import app            # Flask web application
from bot_handler import bot_app  # Telegram bot application
import scheduler                # Reminder scheduler module

# ----------------------------
# Run Flask App
# ----------------------------
def run_flask():
    print("🌐 Flask web server starting...")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)


# ----------------------------
# Run Telegram Bot
# ----------------------------
def run_bot():
    print("🤖 Telegram bot is running...")
    bot_app.run_polling()


# ----------------------------
# Run Scheduler
# ----------------------------
def run_scheduler():
    print("🕒 Scheduler started (checks tasks every 60 seconds)...")
    scheduler.run_loop_forever()


# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    processes = []

    for target in (run_flask, run_bot, run_scheduler):
        p = multiprocessing.Process(target=target)
        p.start()
        processes.append(p)

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("🛑 Shutting down all processes...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
