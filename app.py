import hashlib
import sqlite3

from flask import Flask, request, render_template, redirect, session, abort
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = '10764a32f083da83643be57e1458adfd'
app.config['SESSION_PERMANENT'] = True

Session(app)

connection = sqlite3.connect("data/users.sqlite", check_same_thread=False)
cursor = connection.cursor()


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        cursor.execute("SELECT password FROM users WHERE username=?", [username])
        result = cursor.fetchone()
        if not result:
            return redirect('/login')
        password_hash, = result
        if hashlib.md5(request.form.get('password').encode()).hexdigest() == password_hash:
            session["username"] = request.form.get("username")
            cursor.execute("SELECT role, name FROM users INNER JOIN teams on team_id=teams.id WHERE username=?",
                           [session["username"]])
            session["role"], session["team_name"] = cursor.fetchone()
            
            session['username'] = username
            return redirect("/")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect("/login")


@app.route('/')
def index():
    if not session.get("username"):
        return redirect("/login")

    if session.get("role") == 'manager':
        cursor.execute("SELECT role, name FROM users INNER JOIN teams on team_id=teams.id WHERE username=?",
                       [session["username"]])

    return render_template('index.html', username=session["username"], role=session.get("role"),
                           team_name=session.get("team_name"))


@app.route('/manageUsers')
def manage_users():
    if not session.get("username"):
        return redirect("/login")
    if session.get("role") != 'manager':
        abort(403)

    cursor.execute("SELECT username FROM users WHERE username!='admin'")
    users = cursor.fetchall()
    return render_template('manageUsers.html', users=users)


@app.route('/manageManagers')
def manege_managers():
    if not session.get("username"):
        return redirect("/login")
    if session.get("username") != 'admin':
        abort(403)

    cursor.execute("SELECT username FROM users WHERE role='manager'")
    managers = cursor.fetchall()
    return render_template('manageManagers.html', managers=managers)


if __name__ == '__main__':
    app.run(debug=True)
