from os.path import join as join_path, abspath
from datetime import datetime
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_method

from src import db
from src.models import AlchemySerializable


class AppState(Enum):
    not_enabled = 'not enabled'
    running = 'running'
    stopped = 'stop'
    stopping = 'stopping'
    starting = 'starting'
    fatal = 'fatal'
    exited = 'exited'
    backoff = 'backoff'


class AppType(Enum):
    python = 'python'
    # php = 'php'
    # nodejs = 'nodejs'


class Application(db.Model, AlchemySerializable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    enabled = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.Enum(AppType), nullable=False)

    entry_point = db.Column(db.String(), nullable=True)
    port = db.Column(db.Integer())

    state = db.Column(db.Enum(AppState), default=AppState.not_enabled)

    @hybrid_method
    def get_supervisor_name(self):
        return self.user.username + "-" + self.name

    @hybrid_method
    def get_app_ftp_dir(self):
        user_home = self.user.get_ftp_home_dir()
        return abspath(join_path(user_home, self.name))

    @hybrid_method
    def get_supervisor_conf_path(self):
        """
        return the path to the supervisor conf file of this application
         """
        return join_path(self.user.get_supervisor_conf_dir(), self.username, f"{self.name}.ini")
