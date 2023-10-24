import sqlite3
from flask import Flask, redirect, render_template, session, url_for, request


app = Flask(__name__)
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"


@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html")
    return redirect(url_for("auth"))


@app.route("/auth")
def auth():
    if "username" in session:
        return redirect(url_for("index"))
    return render_template("auth.html")


@app.route("/api/auth", methods=["POST"])
def authenticate():
    user = request.form["user"]
    password = request.form["pass"]
    conn = sqlite3.connect("db/data.sqlite")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE name = ? AND pass = ?",
        (user,
        password)
    )
    res = cursor.fetchone()
    conn.close()

    if res[0] != 0:
        session["username"] = request.form["user"]
        return redirect(url_for("index"))
    return redirect(url_for("auth"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("auth"))


if __name__ == "__main__":
    app.run("127.0.0.1", 80, True)
