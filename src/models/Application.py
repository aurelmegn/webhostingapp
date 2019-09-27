from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method

from src import db
from src.models import AlchemySerializable


class Application(db.Model, AlchemySerializable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    enabled = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.String(), nullable=False)


    @hybrid_method
    def get_supervisor_name(self):
        return self.user.username + "-" + self.name
