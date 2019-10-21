from datetime import datetime
from os.path import abspath
from os.path import join as join_path
from xmlrpc.client import Fault

from sqlalchemy.ext.hybrid import hybrid_method

from src import app, db, supervisor
from src.utils.HelperClass import AlchemySerializable, AppState, AppType


class Application(db.Model, AlchemySerializable):
    id = db.Column(db.Integer, primary_key=True)
    enabled = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    have_started_once = db.Column(db.Boolean, default=False)

    name = db.Column(db.String(), nullable=False)
    type = db.Column(db.Enum(AppType), nullable=False, default=AppType.python37)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    description = db.Column(db.Text())
    entrypoint = db.Column(db.String())
    domain_name = db.Column(db.String())
    callable = db.Column(db.String())

    payment_plans = db.relationship(
        "PaymentPlan",
        backref="application",
        lazy=True,
        # cascade="all, delete-orphan",
    )

    action_histories = db.relationship(
        "AppActionHistory",
        backref="application",
        lazy=True,
        cascade="all, delete-orphan",
    )
    state_histories = db.relationship(
        "AppStateHistory",
        backref="application",
        lazy=True,
        cascade="all, delete-orphan",
    )

    @property
    def state(self):
        """get the current state of the application,
            if the getProcessInfo failed, it's surely mean that the application has never been started
        """
        try:
            process_info = supervisor.getProcessInfo(self.get_supervisor_name())
            state = process_info.get("state")

            return AppState(state)
        except (Fault, Exception):
            return AppState.never_started

    @property
    def port(self):
        """get the port the application should listen on
        """
        return 8000 + self.id

    @hybrid_method
    def get_supervisor_name(self):
        return self.user.username + "-" + self.name

    @hybrid_method
    def get_app_ftp_dir(self):
        user_home = self.user.get_ftp_home_dir()
        return abspath(join_path(user_home, self.name))

    @hybrid_method
    def get_app_ftp_content_dir(self):
        user_home = self.user.get_ftp_home_dir()
        return abspath(join_path(user_home, self.name, "content"))

    @hybrid_method
    def get_supervisor_conf_path(self):
        """
        return the path to the supervisor conf file of this application
         """
        return join_path(self.user.get_supervisor_conf_dir(), f"{self.name}.ini")

    @hybrid_method
    def get_uwsgi_conf_path(self):
        """
        return the path to the uwsgi conf file of this application
         """
        return f"{self.name}.uwsgi.ini"

    @hybrid_method
    def get_abs_uwsgi_conf_path(self):
        """
        return the path to the uwsgi conf file of this application
         """
        return join_path(self.get_app_ftp_dir(), f"{self.name}.uwsgi.ini")

    @hybrid_method
    def get_abs_nginx_conf_path(self):
        """
        return the path to the nginx conf file of this application
         """
        nginx_dir = app.config.get("NGINX_SITE_CONF")
        return join_path(nginx_dir, f"{self.get_supervisor_name()}.conf")

    @hybrid_method
    def get_out_log_path(self):
        """
        return the path to the log conf file of this application
         """
        return f"{self.name}.out.log"

    @hybrid_method
    def get_out_for_supervisor_log_path(self):
        """
        return the path to the log conf file of this application
         """
        return join_path(self.get_app_ftp_dir(), f"{self.name}.out.log")

    @hybrid_method
    def get_err_log_path(self):
        """
        return the path to the supervisor conf file of this application
         """
        return join_path(self.user.get_supervisor_conf_dir(), f"{self.name}.err.log")

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
            and self.domain_name is not None
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

    @hybrid_method
    def can_act(self):
        print(self.can_start())
        return self.can_stop() or self.can_start() or self.can_restart()

    @hybrid_method
    def can_execute_command(self):

        return True
