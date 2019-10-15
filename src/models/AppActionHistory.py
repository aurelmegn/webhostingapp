from datetime import datetime

from src import db
from src.models.Application import AppState


class AppActionHistory(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    action = db.Column(db.String(), nullable=False)
    new_state = db.Column(db.Enum(AppState), nullable=False)
    old_state = db.Column(db.Enum(AppState), nullable=False)

    application_id = db.Column(db.Integer, db.ForeignKey("application.id"))
