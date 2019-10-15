# Import flask and template operators
import logging
from flask import Flask
from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_webpackext import FlaskWebpackExt, WebpackBundleProject
from os import makedirs
from os.path import join, isdir

from src.utils.jinja_filters import date_format_datetime, fa_icon_flash_filter, state_to_str, from_state_color

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
app.jinja_env.filters["fa_icon"] = fa_icon_flash_filter
app.jinja_env.filters["state_str"] = state_to_str
app.jinja_env.filters["state_color"] = from_state_color
# debug toolbar
toolbar = DebugToolbarExtension(app)
FlaskWebpackExt(app)

# flask admin
admin = Admin(app, name='myapp', template_mode='bootstrap3', url='/wtf')
# additional configurations for the app

# log handlers

# logging.basic_config(level=os.environ.get("LOGLEVEL", "CRITICAL"), handlers=)
# app_log_handler = logging.StreamHandler()
# app_log_handler.setLevel(logging.DEBUG)

# log file
log_dir = "./var/log"
if not isdir(log_dir):
    makedirs(log_dir)

if app.config.get("ENV").startswith("dev"):
    log_file = "dev.log"
else:
    log_file = "prod.log"
log_file = join(log_dir, log_file)

app_file_log_handler = logging.FileHandler(log_file)
app_file_log_handler.setLevel(logging.DEBUG)

app.logger.addHandler(app_file_log_handler)

app.logger.setLevel(logging.DEBUG)
# app.logger.addHandler(app_log_handler)

# Sample HTTP error handling
# app.logger.error("++++++" )

# supervisor api var
from xmlrpc.client import ServerProxy, Fault

server = ServerProxy("http://localhost:9001/RPC2")
supervisor = server.supervisor

# exit if not able to connect to supervisor running instance
try:
    supervisor.getState()
except (OSError, Fault) as e:
    app.logger.error("Unable to connect to supervisor. Exiting ...")
    app.logger.error(e)
    exit(1)

from src.controllers import *

# from src.models import roles_users
from src.models.User import User
from src.models.Role import Role
# from src.models.AppHistory import AppHistory

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# from admin interface
import src.admin_views


@app.errorhandler(404)
def not_found(error):
    app.logger.error(error)
    return render_template("errors/404.jinja", error=error), 404


@app.errorhandler(500)
def not_found(error):
    app.logger.error(error)
    return render_template("errors/500.jinja", error=error), 500


@app.before_first_request
def before_first_request():
    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='End user')

    db.session.commit()

