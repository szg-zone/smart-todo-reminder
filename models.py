from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# ----------------------------
# USER MODEL
# ----------------------------
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    telegram_chat_id = db.Column(db.String(100), nullable=True)

    tasks = db.relationship('Task', backref='user', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


# ----------------------------
# TASK MODEL
# ----------------------------
class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default="Pending")
    notified = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"
