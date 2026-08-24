import threading


class SquaredSumWorker(threading.Thread):
    """Thread that calculates and prints the sum of squares from 0 to n-1."""
    def __init__(self, n, **kwargs):
        self._n = n
        super().__init__(**kwargs)

        self.start()

    def _calculate_sum_squares(self):
        """Compute the sum of squares iteratively from 0 to n-1."""
        sum_squares = 0
        for i in range(self._n):
            sum_squares += i ** 2

        print(sum_squares)

    def run(self):
        """Execute the sum of squares calculation in the thread."""
        self._calculate_sum_squares()