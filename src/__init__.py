# Import flask and template operators
import logging
from flask import Flask, got_request_exception
from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_webpackext import FlaskWebpackExt, WebpackBundleProject
from os import makedirs
from os.path import join, isdir
from dynaconf import FlaskDynaconf

from src.utils.jinja_filters import date_format_datetime, fa_icon_flash_filter, state_to_str, from_state_color

webpack_project = WebpackBundleProject(
    __name__, project_folder="assets", config_path="./public/entrypoint.json"
)

app = Flask(__name__, static_folder="public")
FlaskDynaconf(app)
FlaskWebpackExt(app)

app.config.update(dict(WEBPACKEXT_PROJECT=webpack_project))

# Sql alchemy
db = SQLAlchemy(app)

# Template engine setup
app.jinja_env.filters["datetime"] = date_format_datetime
app.jinja_env.filters["fa_icon"] = fa_icon_flash_filter
app.jinja_env.filters["state_str"] = state_to_str
app.jinja_env.filters["state_color"] = from_state_color

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
    
    from flask_debugtoolbar import DebugToolbarExtension

    # debug toolbar
    toolbar = DebugToolbarExtension(app)

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

server = ServerProxy("http://localhost:7000/RPC2")
supervisor = server.supervisor

# exit if not able to connect to supervisor running instance
try:
    supervisor.getState()
except (OSError, Fault) as e:
    app.logger.error("Unable to connect to supervisor. Exiting ...")
    app.logger.error(e)
    exit(1)

# from src.models import roles_users
from src.models.User import User
from src.models.Role import Role
# from src.models.AppHistory import AppHistory

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from src.controllers import *

from src.controllers.settings import settings_bp
from src.controllers.dashboard import dashboard_bp
from src.controllers.docs import docs_bp
from src.controllers.blog import blog_bp

app.register_blueprint(settings_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(docs_bp)
app.register_blueprint(blog_bp)

# from admin interface
import src.admin_views


@app.before_first_request
def before_first_request():
    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='End user')
    user_datastore.find_or_create_role(name='staff', description='Staff')

    db.session.commit()


import rollbar
import rollbar.contrib.flask
import os

if app.config.get("ENV").startswith("prod"):
    @app.before_first_request
    def init_rollbar():
        """init rollbar module"""
        rollbar.init(
            # access token for the demo app: https://rollbar.com/demo
            'f981e8a11b4d49958c120d94094dfd00',
            # environment name
            app.config.get("ENV"),
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False)

        # send exceptions from `app` to rollbar, using flask's signal system.
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

