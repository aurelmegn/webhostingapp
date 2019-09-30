from src import app
from flask import render_template
from flask_security import login_required, roles_required


@app.route("/")
@login_required
@roles_required("user")
def index():
    return render_template("default/index.jinja")
