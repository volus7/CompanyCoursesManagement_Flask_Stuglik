import hashlib
import sqlite3

from flask import Flask, request, render_template, redirect, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect("data/users.sqlite", check_same_thread=False)
cursor = connection.cursor()


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        cursor.execute("SELECT password FROM users WHERE username=?", [request.form.get('username')])
        result = cursor.fetchone()
        if not result:
            return redirect('/login')
        password_hash, = result
        if hashlib.md5(request.form.get('password').encode()).hexdigest() == password_hash:
            session["username"] = request.form.get("username")
            return redirect("/")
    return render_template("login.html")


@app.route('/')
def index():
    if not session.get("username"):
        return redirect("/login")
    cursor.execute("SELECT role, name FROM users INNER JOIN teams on team_id=teams.id WHERE username=?", [session["username"]])
    role, team_name = cursor.fetchone()
    if role == 'manager':
        cursor.execute("SELECT role, name FROM users INNER JOIN teams on team_id=teams.id WHERE username=?",
                       [session["username"]])

    return render_template('index.html', username=session["username"], role=role, team_name=team_name)


if __name__ == '__main__':
    app.run()
