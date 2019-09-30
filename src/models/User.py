from os.path import join as join_path, abspath

from datetime import datetime

from flask_security import UserMixin
from sqlalchemy.ext.hybrid import hybrid_method

from src import db, app
from . import roles_users, AlchemySerializable


class User(db.Model, UserMixin, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    # trace properties
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(15))
    current_login_ip = db.Column(db.String(15))
    login_count = db.Column(db.Integer())

    ftp_quota = db.Column(db.Numeric(), default=1)
    # application

    applications = db.relationship("Application", backref="user", lazy=False)

    def __repr__(self):
        return "<User %r>" % self.username

    @hybrid_method
    def get_ftp_home_dir(self):
        base_path = app.config.get('FTP_BASE_DIR')
        base_path = abspath(base_path)

        return join_path(base_path, self.username)

    @hybrid_method
    def get_supervisor_conf_dir(self):
        """generate the path to the user's conf directory for supervisor applications """
        base_path = app.config.get('SUPERVISOR_CONFIG_DIR')
        base_path = abspath(base_path)

        return join_path(base_path, "programs", self.username)
