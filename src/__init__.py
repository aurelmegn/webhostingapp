# Import flask and template operators
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_webpackext import FlaskWebpackExt
from src.utils.format_datetime import date_format_datetime
from flask_security import Security, SQLAlchemyUserDatastore

app = Flask(__name__, static_folder="public")

# Configurations
app.config.from_object("config")

# Sql alchemy
db = SQLAlchemy(app)

# Template engine setup
app.jinja_env.filters["datetime"] = date_format_datetime

# debug toolbar
toolbar = DebugToolbarExtension(app)
FlaskWebpackExt(app)

from src.controllers import *
from src.models.User import User
from src.models.Role import Role

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.jinja"), 404


@app.errorhandler(500)
def not_found(error):
    return render_template("errors/500.jinja"), 500
