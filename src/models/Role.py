from flask_security import RoleMixin

from src import db
from src.utils.HelperClass import AlchemySerializable


class Role(db.Model, RoleMixin, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
