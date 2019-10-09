from flask import render_template

from src import app


@app.route("/blog")
def blog():
    return render_template("default/blog.jinja")
