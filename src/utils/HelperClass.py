from enum import Enum


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

