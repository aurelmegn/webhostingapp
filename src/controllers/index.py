from src import app
from flask import render_template, request
from flask_security import login_required


@app.route("/")
@login_required
def index():
    return render_template("default/index.jinja")
