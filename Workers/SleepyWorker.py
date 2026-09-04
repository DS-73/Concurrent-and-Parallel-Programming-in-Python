"""
SleepyWorker - I/O-Bound Thread Worker

A simple Thread subclass that sleeps for a specified duration.
Used to simulate I/O-bound operations (network requests, file I/O, etc.).

Purpose:
    - Demonstrate Thread subclass pattern
    - Show daemon thread usage for background tasks
    - Provide reusable sleep worker for pipeline examples
"""

import threading
import time


class SleepyWorker(threading.Thread):
    """
    Thread that sleeps for a specified number of seconds.

    Inherits from threading.Thread and overrides run() method.
    Auto-starts on instantiation for convenience.

    Attributes:
        _seconds: Duration to sleep in seconds.
    """

    def __init__(self, seconds: int, **kwargs) -> None:
        """
        Initialize and start the sleep worker.

        Args:
            seconds: Number of seconds to sleep.
            **kwargs: Passed to Thread.__init__ (e.g., daemon=True).
        """
        self._seconds = seconds
        super().__init__(**kwargs)
        self.start()  # Begin execution immediately

    def _sleep_a_little(self) -> None:
        """Sleep for the configured duration."""
        time.sleep(self._seconds)

    def run(self) -> None:
        """Thread entry point: execute the sleep operation."""
        self._sleep_a_little()