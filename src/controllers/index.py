from flask import redirect, render_template, session
from flask_security import logout_user
from werkzeug.exceptions import HTTPException, NotFound

from src import app


@app.route("/")
def index():
    return render_template("default/index.jinja")


@app.route("/logout")
def logout():
    logout_user()
    session.clear()

    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    app.logger.error(error)
    return render_template("errors/404.jinja", error=error), 404


@app.errorhandler(500)
def not_found(error):
    app.logger.error(error)
    return render_template("errors/500.jinja", error=error), 500


@app.errorhandler(HTTPException)
def not_found(error):
    app.logger.error(error)
    return render_template("errors/exception.jinja", error=error), 500
