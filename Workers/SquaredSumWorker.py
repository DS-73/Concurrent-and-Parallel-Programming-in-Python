"""
SquaredSumWorker - CPU-Bound Thread Worker

A Thread subclass that calculates the sum of squares from 0 to n-1.
Used to simulate CPU-bound computational work.

Purpose:
    - Demonstrate Thread subclass for CPU-bound tasks
    - Show auto-start pattern for worker threads
    - Provide reusable computation worker for pipeline examples

Note: Due to Python's GIL, multiple instances won't run truly
      in parallel on multi-core systems. Use multiprocessing for
      true CPU parallelism.
"""

import threading


class SquaredSumWorker(threading.Thread):
    """
    Thread that calculates and prints the sum of squares from 0 to n-1.

    Attributes:
        _n: Upper bound (exclusive) for the summation range.
    """

    def __init__(self, n: int, **kwargs) -> None:
        """
        Initialize and start the computation worker.

        Args:
            n: Calculate sum of squares from 0 to n-1.
            **kwargs: Passed to Thread.__init__.
        """
        self._n = n
        super().__init__(**kwargs)
        self.start()  # Begin execution immediately

    def _calculate_sum_squares(self) -> None:
        """Compute the sum of squares iteratively and print result."""
        sum_squares = 0
        for i in range(self._n):
            sum_squares += i ** 2
        print(f"Sum of squares (0 to {self._n - 1}): {sum_squares}")

    def run(self) -> None:
        """Thread entry point: execute the sum of squares calculation."""
        self._calculate_sum_squares()