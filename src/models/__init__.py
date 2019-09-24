import json

from src import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            # an SqlAlchemy class
            fields = {}
            for field in [x for x in dir(o) if not (x.startswith('_') or
                                                    x.startswith('query')) and x != 'metadata']:
                data = o.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, o)


class AlchemySerializable:

    def __json__(self):
        return json.dumps(self, cls=AlchemyEncoder)
