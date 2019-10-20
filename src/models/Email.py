from src import db
from src.utils.HelperClass import AlchemySerializable


class Email(db.Model, AlchemySerializable):
    id = db.Column(db.Integer(), primary_key=True)

    label = db.Column(db.String(120), unique=True, nullable=False)
    is_primary = db.Column(db.Boolean(), default=False)
    receive_notifications = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
