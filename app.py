from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task
from config import Config
import os

# ---------------------------
# 1️⃣ Flask App Initialization
# ---------------------------
app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

# ---------------------------
# 2️⃣ Flask-Login Setup
# ---------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------------
# 3️⃣ Routes
# ---------------------------

@app.route('/')
def home():
    return render_template('login.html')


# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('⚠️ Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('✅ Account created successfully! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("✅ Logged in successfully!")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')


# -------- DASHBOARD --------
@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.telegram_chat_id:
        telegram_link = f"https://t.me/SmartToDoSharvinBot?start={current_user.id}"
        return render_template('link_telegram.html', telegram_link=telegram_link)

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username, tasks=tasks)


# -------- CHECK TELEGRAM LINK --------
@app.route('/check_telegram_link')
@login_required
def check_telegram_link():
    db.session.refresh(current_user)
    if current_user.telegram_chat_id:
        flash("✅ Telegram linked successfully! You can now use the app.")
    else:
        flash("❌ Still not linked. Please link your Telegram account first.")
    return redirect(url_for('dashboard'))


# -------- ADD TASK --------
@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form.get('time', None)

        new_task = Task(
            title=title,
            description=description,
            date=date,
            time=time,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('✅ Task added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_task.html')


# -------- DELETE TASK --------
@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("⚠️ You can't delete someone else's task!")
        return redirect(url_for('dashboard'))
    db.session.delete(task)
    db.session.commit()
    flash('🗑️ Task deleted successfully.')
    return redirect(url_for('dashboard'))


# -------- DELETE ACCOUNT --------
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user

    # Delete all the user's tasks first
    Task.query.filter_by(user_id=user.id).delete()

    # Delete the user itself
    db.session.delete(user)
    db.session.commit()

    logout_user()
    flash("🧹 Your account and all tasks have been deleted successfully.", "info")

    return redirect(url_for('register'))


# -------- LOGOUT --------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('👋 You have been logged out.')
    return redirect(url_for('login'))


# -------- MAIN --------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
