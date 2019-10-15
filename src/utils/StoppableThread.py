import threading


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, target=None, args=None, daemon=False):
        super(StoppableThread, self).__init__(target=target, args=args, daemon=daemon)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        super(StoppableThread, self).join(*args, **kwargs)

    def run(self):
        while not self._stop_event.is_set():
            super(StoppableThread, self).run()
