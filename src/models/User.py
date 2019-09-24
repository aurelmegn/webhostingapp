from datetime import datetime

from flask_login import UserMixin

from src import db
from . import roles_users, AlchemySerializable


class User(db.Model, UserMixin, AlchemySerializable):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    # trace properties
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(15))
    current_login_ip = db.Column(db.String(15))
    login_count = db.Column(db.Integer)

    # application

    applications = db.relationship("Application", backref="user", lazy=False)

    def __repr__(self):
        return "<User %r>" % self.username
