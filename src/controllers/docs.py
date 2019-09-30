from flask import render_template

from src import app


@app.route("/docs")
def docs():
    return render_template("default/docs.jinja")
