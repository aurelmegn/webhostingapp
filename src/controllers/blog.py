from flask import render_template
from flask_login import login_required
from flask_security import roles_required

from src import app


@app.route("/blog")
@login_required
@roles_required("user")
def blog():
    return render_template("default/blog.jinja")
