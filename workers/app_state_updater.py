import atexit

from src.models import AppStateHistory
from src import Application, db
from src.utils.StoppableThread import StoppableThread
from time import sleep

threads = []


def run_threads():
    # app_state_updater()
    start_threads(app_state_updater)

    atexit.register(stop_threads)


def app_state_updater():
    while True:

        sleep(1800)  # 1800 s=>30 mins

        app_count = Application.query.filter_by(enabled=True, have_started_once=True).count()

        apps = Application.query.filter_by(enabled=True, have_started_once=True).all()

        for app in apps:
            state = app.state

            state_history = AppStateHistory(application=app, state=state)
            db.session.add(state_history)

        db.session.commit()
        exit(0)


def start_threads(f, args=[]):
    t = StoppableThread(target=f, args=args, daemon=True)
    t.start()
    threads.append(t)


def stop_threads():
    for thread in threads:
        thread.stop()
