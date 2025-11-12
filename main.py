# main.py
import multiprocessing
import time

from app import app            # your Flask app
from bot_handler import bot_app  # your telegram Application (bot)
import scheduler                # your scheduler module (must contain run_scheduler())

def run_flask():
    # run flask dev server; disable reloader to avoid double-start
    app.run(debug=True, use_reloader=False)

def run_bot():
    print("🤖 Telegram bot is running...")
    # run_polling is blocking, run in its own process
    bot_app.run_polling()

def run_scheduler():
    print("🕒 Scheduler started...")
    # Ideally scheduler provides a blocking function to start loop
    scheduler.run_loop_forever()  # we'll create this in scheduler.py

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
        print("Shutting down...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
