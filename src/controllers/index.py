from flask import redirect, render_template, session

from flask_security import logout_user
from src import app


@app.route("/")
def index():
    return render_template("default/index.jinja")


@app.route("/logout")
def logout():
    logout_user()
    session.clear()

    return redirect("/")
