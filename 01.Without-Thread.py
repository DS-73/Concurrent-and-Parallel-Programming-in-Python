"""
Sequential Execution Example

This module demonstrates sequential task execution without threading.
It performs CPU-bound (sum of squares) and I/O-bound (sleep) tasks one after another.

Purpose:
    - Baseline for comparing sequential vs concurrent execution
    - Shows how tasks block each other when run sequentially
"""

import time


def calculate_sum_squares(n: int) -> None:
    """
    Calculate and print the sum of squares from 0 to n-1.

    This is a CPU-bound operation that performs intensive computation.

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

    This is an I/O-bound operation that simulates waiting (e.g., network request).

    Args:
        seconds: Number of seconds to sleep.
    """
    time.sleep(seconds)


def main() -> None:
    """
    Run sequential tasks: calculate sum of squares and sleep delays.

    Tasks are executed one at a time:
    1. First runs 5 sum-of-squares calculations with increasing workloads
    2. Then runs 5 sleep operations with increasing durations

    Total time = sum of all individual task times (no overlap).
    """
    # CPU-bound tasks - run sequentially
    square_time_start = time.time()
    for i in range(5):
        calculate_sum_squares((i + 1) * 1_000_000)

    print(f"Sum of Squares Task: {round(time.time() - square_time_start, 1)}s")

    # I/O-bound tasks - run sequentially
    sleep_time_start = time.time()
    for i in range(1, 6):
        sleep_a_little(i)

    print(f"Sleeping Task: {round(time.time() - sleep_time_start, 1)}s")


if __name__ == "__main__":
    main()