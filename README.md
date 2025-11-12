
# 🚀 SmartToDo Reminder 🚀

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-v2.3.2-green)](https://flask.palletsprojects.com/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot-orange)](https://core.telegram.org/bots/api)

## ✨ Introduction

SmartToDo Reminder is a powerful and flexible task management application that combines the convenience of a web interface with the timely reminders of a Telegram bot.  It allows users to create, manage, and receive notifications for their tasks, ensuring nothing slips through the cracks. This project is designed for individuals looking to boost their productivity and stay organized.

## 🌟 Features

*   **Web Interface:** User-friendly web application built with Flask for creating, viewing, and deleting tasks.
*   **Telegram Integration:** Receive task reminders directly on Telegram via a bot.
*   **User Authentication:** Secure user accounts with login and registration functionality.
*   **Task Scheduling:**  Set due dates and times for tasks to receive timely reminders.
*   **Database Persistence:** Tasks are stored securely using SQLite.
*   **Account Management:** Users can delete their accounts and associated data.
*   **Clean & Responsive Design:**  A visually appealing and responsive user interface.

## 🛠️ Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/[YOUR_USERNAME]/smart-todo-reminder.git
    cd smart-todo-reminder
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    *   Create a `.env` file in the root directory of the project.
    *   Add the following variables:

        ```
        SECRET_KEY=your_secret_key  # Replace with a strong secret key
        TELEGRAM_BOT_TOKEN=your_telegram_bot_token  # Replace with your Telegram bot token
        ```

5.  **Initialize the database:**

    ```bash
    python
    >>> from models import db
    >>> db.create_all()
    >>> exit()
    ```

## 🚀 Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

    This will start the web server, typically accessible at `http://127.0.0.1:5000/`.

2.  **Run the Telegram bot:**

    ```bash
    python bot_handler.py
    ```

    This will start the Telegram bot, which will listen for commands and send reminders.

3.  **Access the web application:**

    *   Open your web browser and navigate to `http://127.0.0.1:5000/`.
    *   Register a new account or log in with an existing one.
    *   Add tasks with titles and due dates/times.

4.  **Interact with the Telegram bot:**

    *   Start a chat with your bot on Telegram.
    *   Use the `/start` command to initialize the bot.
    *   The bot will send reminders for your tasks at the specified times.

## 🤝 Contributing

We welcome contributions to SmartToDo Reminder!  Here's how you can get involved:

1.  **Fork the repository.**
2.  **Create a new branch:**

    ```bash
    git checkout -b feature/your-feature-name
    ```

3.  **Make your changes.**
4.  **Commit your changes:**

    ```bash
    git commit -m "Add your descriptive commit message"
    ```

5.  **Push to the branch:**

    ```bash
    git push origin feature/your-feature-name
    ```

6.  **Create a pull request.**

Please ensure your code follows the project's style guidelines and includes appropriate tests.

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  See the `LICENSE` file for more information.

## 📄 Files Overview

*   **`app.py`**:  Main Flask application file, handles web routes and logic.
*   **`bot_handler.py`**:  Handles the Telegram bot functionality, including command processing and sending reminders.
*   **`config.py`**:  Configuration file for Flask and database settings.
*   **`main.py`**:  Entry point for the application, starts both the Flask app and the Telegram bot.
*   **`models.py`**:  Defines the database models for User and Task.
*   **`scheduler.py`**:  Responsible for scheduling and sending task reminders.
*   **`static/style.css`**:  CSS file for styling the web application.
*   **`templates/add_task.html`**:  HTML template for the add task page.
*   **`templates/base.html`**:  Base HTML template for all pages.
*   **`templates/dashboard.html`**:  HTML template for the user dashboard.

## 🙏 Acknowledgements

*   Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
*   Flask-SQLAlchemy: [https://flask-sqlalchemy.readthedocs.io/](https://flask-sqlalchemy.readthedocs.io/)
*   Flask-Login: [https://flask-login.readthedocs.io/](https://flask-login.readthedocs.io/)
*   python-telegram-bot: [https://github.com/python-telegram-bot/python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
*   Bootstrap: [https://getbootstrap.com/](https://getbootstrap.com/)

---

✨ Happy Tasking! ✨


## License
This project is licensed under the **MIT** License.

---
🔗 GitHub Repo: https://github.com/szg-zone/smart-todo-reminder
