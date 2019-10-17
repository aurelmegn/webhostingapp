import json
from enum import Enum
from sqlalchemy.ext.declarative import DeclarativeMeta


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


class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            # an SqlAlchemy class
            fields = {}
            for field in [
                x
                for x in dir(o)
                if not (x.startswith("_") or x.startswith("query")) and x != "metadata"
            ]:
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


class AppType(Enum):
    python35 = "python_3.5"
    python36 = "python_3.6"
    python37 = "python_3.7"
    # php = 'php'
    # nodejs = 'nodejs'
