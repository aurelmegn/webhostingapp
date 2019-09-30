# Import flask and template operators
from flask import Flask, render_template
from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_webpackext import FlaskWebpackExt, WebpackBundleProject

from .utils.format_datetime import date_format_datetime

myproject = WebpackBundleProject(
    __name__, project_folder="assets", config_path="./public/entrypoint.json"
)

app = Flask(__name__, static_folder="public")

app.config.update(dict(WEBPACKEXT_PROJECT=myproject))

# Configurations
app.config.from_object("config")

# Sql alchemy
db = SQLAlchemy(app)

# Template engine setup
app.jinja_env.filters["datetime"] = date_format_datetime

# debug toolbar
toolbar = DebugToolbarExtension(app)
FlaskWebpackExt(app)

# flask admin

admin = Admin(app, name='myapp', template_mode='bootstrap3', url='/wtf')

# additional configurations for the app

# supervisor api var
from xmlrpc.client import ServerProxy

server = ServerProxy("http://localhost:9001/RPC2")
supervisor = server.supervisor

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


@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='End user')

    db.session.commit()
