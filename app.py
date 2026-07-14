from datetime import date, timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

app = Flask(__name__)
app.secret_key = "ilovecomputerscience"

db = SQL("sqlite:///habitgarden.db")

# Portions of this code (Flask routes, streak logic, SQL schema) were developed with assistance from Claude (Anthropic AI). All logic was reviewed, tested, and understood before submission.

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_stage(streak):
    if streak == 0:
        return "seed"
    elif streak <= 2:
        return "sprout"
    elif streak <= 6:
        return "growing"
    elif streak <= 13:
        return "blooming"
    else:
        return "flourishing"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Username and password are required", 400

        existing = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing:
            return "Username already taken", 400

        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return "Invalid username or password", 403

        session["user_id"] = rows[0]["id"]
        return redirect("/habits")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect("/habits")
    return redirect("/login")


@app.route("/habits")
@login_required
def habits():
    user_habits = db.execute("SELECT * FROM habits WHERE user_id = ?", session["user_id"])
    for h in user_habits:
        h["stage"] = get_stage(h["streak"])
    return render_template("habits.html", habits=user_habits)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return "Habit name is required", 400
        db.execute(
            "INSERT INTO habits (user_id, name, streak) VALUES (?, ?, 0)",
            session["user_id"], name
        )
        return redirect("/habits")

    return render_template("add_habit.html")


@app.route("/delete/<int:habit_id>")
@login_required
def delete(habit_id):
    db.execute("DELETE FROM checkins WHERE habit_id = ?", habit_id)
    db.execute("DELETE FROM habits WHERE id = ? AND user_id = ?", habit_id, session["user_id"])
    return redirect("/habits")


@app.route("/checkin/<int:habit_id>")
@login_required
def checkin(habit_id):
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    rows = db.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        habit_id, session["user_id"]
    )
    if not rows:
        return redirect("/habits")
    habit = rows[0]

    already = db.execute(
        "SELECT * FROM checkins WHERE habit_id = ? AND date = ?", habit_id, today
    )
    if already:
        return redirect("/habits")

    if habit["last_checkin_date"] == yesterday:
        new_streak = habit["streak"] + 1
    else:
        new_streak = max(habit["streak"] - 1, 0) + 1

    db.execute(
        "INSERT INTO checkins (habit_id, date, completed) VALUES (?, ?, 1)",
        habit_id, today
    )
    db.execute(
        "UPDATE habits SET streak = ?, last_checkin_date = ? WHERE id = ?",
        new_streak, today, habit_id
    )

    return redirect("/habits")


@app.route("/history/<int:habit_id>")
@login_required
def history(habit_id):
    checkins = db.execute(
        "SELECT date FROM checkins WHERE habit_id = ? ORDER BY date DESC LIMIT 7",
        habit_id
    )
    return render_template("history.html", checkins=checkins)


if __name__ == "__main__":
    app.run(debug=True)
