import time
import threading


class SleepyWorker(threading.Thread):
    """Thread that sleeps for a specified number of seconds."""
    def __init__(self, seconds, **kwargs):
        self._seconds = seconds
        super().__init__(**kwargs)

        self.start()

    def _sleep_a_little(self):
        """Sleep for the configured number of seconds."""
        time.sleep(self._seconds)

    def run(self):
        """Execute the sleep in the thread."""
        self._sleep_a_little()