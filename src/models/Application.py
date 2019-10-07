from os.path import join as join_path, abspath
from datetime import datetime
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_method
from xmlrpc.client import Fault

from src import db, supervisor
from src.models import AlchemySerializable


class AppState(Enum):
    stopped = 0  # "stop"
    starting = 10  # "starting"
    running = 20  # "running"
    backoff = 30  # "backoff"
    stopping = 40  # "stopping"
    exited = 100  # "exited"
    fatal = 200  # "fatal"
    unknown = 1000  # "unknown"
    never_started = -1  # "never_started"


class AppType(Enum):
    python35 = "python_3.5"
    python36 = "python_3.6"
    python37 = "python_3.7"
    # php = 'php'
    # nodejs = 'nodejs'


class Application(db.Model, AlchemySerializable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    enabled = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.Enum(AppType), nullable=False, default=AppType.python37)

    entrypoint = db.Column(db.String())
    port = db.Column(db.Integer())

    # state = db.Column(db.Enum(AppState), default=AppState.never_started)
    @property
    def state(self):
        """get the current state of the application,
            if the getProcessInfo failed, it's surely mean that the application has never been started
        """
        try:
            process_info = supervisor.getProcessInfo(self.get_supervisor_name())
            state = process_info.get("state")

            return AppState(state)
        except Fault:
            return AppState.never_started

        except Exception:
            return AppState.never_started

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
        return join_path(self.user.get_supervisor_conf_dir(), f"{self.name}.ini")

    @hybrid_method
    def can_start(self):
        """return whether the start action can be applied to the application given it's current state"""

        return (
            True
            if self.state
               in [
                   AppState.stopped,
                   AppState.backoff,
                   AppState.fatal,
                   AppState.exited,
                   AppState.never_started,
               ]
               and self.entrypoint is not None
               and self.enabled is True
            else False
        )

    @hybrid_method
    def can_restart(self):
        """return whether the restart action can be applied to the application given it's current state"""

        return self.can_stop()

    @hybrid_method
    def can_stop(self):
        """return whether the stop action can be applied to the application given it's current state"""

        return True if self.state in [AppState.running] else False

    def can_act(self):
        print(self.can_start())
        return self.can_stop() or self.can_start() or self.can_restart()

    @hybrid_method
    def get_frontend_color(self):

        color = None
        if self.state in [AppState.stopped, AppState.never_started]:
            color = "grey"
        elif self.state == AppState.running:
            color = "green"
        elif self.state in [AppState.exited, AppState.fatal, AppState.backoff]:
            color = "red"
        elif self.state in [AppState.starting]:
            color = "teal"
        elif self.state in [AppState.stopping]:
            color = "orange"
        return color

    def state_to_string(self):

        str_value = None

        if self.state == AppState.stopped:
            str_value = "Stopped"
        if self.state == AppState.starting:
            str_value = "Starting"
        if self.state == AppState.running:
            str_value = "Running"
        if self.state == AppState.backoff:
            str_value = "Backoff"
        if self.state == AppState.stopping:
            str_value = "Stopping"
        if self.state == AppState.exited:
            str_value = "Exited"
        if self.state == AppState.fatal:
            str_value = "Fatal"
        if self.state == AppState.unknown:
            str_value = "Unknown"
        if self.state == AppState.never_started:
            str_value = "Never started"

        return str_value
