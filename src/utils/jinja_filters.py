from src.utils.HelperClass import AppState
from babel import dates


def fa_icon_flash_filter(value):
    iname = "fa-"

    if value == "info":
        iname += "info"

    elif value == "error":
        iname += "times-circle-o"

    elif value == "success":
        iname += "check-circle-o"

    elif value == "warning":
        iname += "exclamation-triangle"

    else:
        iname += "circle"
    return iname


def state_to_str(state: AppState) -> str:
    str_value = None

    if state == AppState.stopped:
        str_value = "Stopped"
    if state == AppState.starting:
        str_value = "Starting"
    if state == AppState.running:
        str_value = "Running"
    if state == AppState.backoff:
        str_value = "Backoff"
    if state == AppState.stopping:
        str_value = "Stopping"
    if state == AppState.exited:
        str_value = "Exited"
    if state == AppState.fatal:
        str_value = "Fatal"
    if state == AppState.unknown:
        str_value = "Unknown"
    if state == AppState.never_started:
        str_value = "Never started"

    return str_value


def date_format_datetime(value, format="medium"):
    if format == "full":
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == "medium":
        format = "EE dd.MM.y HH:mm"

    return dates.format_datetime(value, format)


def from_state_color(state):
    color = None
    if state in [AppState.stopped, AppState.never_started]:
        color = "grey"
    elif state == AppState.running:
        color = "green"
    elif state in [AppState.exited, AppState.fatal, AppState.backoff]:
        color = "red"
    elif state in [AppState.starting]:
        color = "teal"
    elif state in [AppState.stopping]:
        color = "orange"
    return color
