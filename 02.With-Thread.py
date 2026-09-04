"""
Threaded Execution Example

This module demonstrates concurrent task execution using Python's threading module.
It runs the same CPU-bound and I/O-bound tasks from 01.Without-Thread.py concurrently.

Purpose:
    - Show how threading enables concurrent execution
    - Demonstrate thread creation, start, and join patterns
    - Compare performance with sequential execution

Note: Due to Python's GIL, CPU-bound threads don't truly run in parallel.
      I/O-bound tasks benefit significantly from threading.
"""

import threading
import time


def calculate_sum_squares(n: int) -> None:
    """
    Calculate and print the sum of squares from 0 to n-1.

    CPU-bound operation - limited by GIL in CPython.

    Args:
        n: The upper bound (exclusive) for the range of integers to square and sum.
    """
    sum_squares = 0
    for i in range(n):
        sum_squares += i ** 2

    print(sum_squares)


def sleep_a_little(seconds: int) -> None:
    """
    Sleep for the specified number of seconds.

    I/O-bound operation - releases GIL during sleep, allowing true concurrency.

    Args:
        seconds: Number of seconds to sleep.
    """
    time.sleep(seconds)


def main() -> None:
    """
    Run threaded tasks: calculate sum of squares and sleep delays concurrently.

    Creates and manages two sets of threads:
    1. Five threads for sum-of-squares calculations (CPU-bound)
    2. Five threads for sleep operations (I/O-bound)

    Uses thread.join() to wait for all threads to complete before timing.
    """
    # CPU-bound tasks - threads created but limited by GIL
    square_time_start = time.time()
    current_threads = []

    for i in range(5):
        t = threading.Thread(
            target=calculate_sum_squares,
            args=((i + 1) * 1_000_000,)
        )
        t.start()
        current_threads.append(t)

    # Wait for all sum-of-squares threads to complete
    for x in current_threads:
        x.join()

    print(f"Sum of Squares Task: {round(time.time() - square_time_start, 1)}s")

    # I/O-bound tasks - threads run truly concurrently
    sleep_time_start = time.time()
    # Reuse the same list for sleep threads
    for i in range(1, 6):
        t = threading.Thread(
            target=sleep_a_little,
            args=(i,)
        )
        t.start()
        current_threads.append(t)

    # Wait for all sleep threads (and any remaining sum threads)
    for x in current_threads:
        x.join()

    print(f"Sleeping Task: {round(time.time() - sleep_time_start, 1)}s")


if __name__ == "__main__":
    main()