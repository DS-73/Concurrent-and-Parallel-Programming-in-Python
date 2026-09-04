"""
Threaded Worker Classes Example

This module demonstrates using custom Thread subclasses (worker pattern)
for encapsulated concurrent tasks. Workers are defined in the Workers/ directory.

Purpose:
    - Show class-based threading with Thread inheritance
    - Demonstrate worker pattern for reusable concurrent tasks
    - Compare with functional threading approach from 02.With-Thread.py
"""

import time
from Workers.SleepyWorker import SleepyWorker
from Workers.SquaredSumWorker import SquaredSumWorker


def main() -> None:
    """
    Run threaded worker examples: squared sum and sleepy workers.

    Creates and manages two types of worker threads:
    1. SquaredSumWorker - CPU-bound calculation workers
    2. SleepyWorker - I/O-bound sleep workers (with daemon=True)

    Daemon threads are killed when main program exits, useful for
    background tasks that shouldn't block program termination.
    """
    # CPU-bound workers - calculate sum of squares
    sum_start_time = time.time()
    threads = []

    for i in range(5):
        # Each worker handles increasing workload
        s = SquaredSumWorker((i + 1) * 1_000_000)
        threads.append(s)

    # Wait for all workers to complete
    for thread in threads:
        thread.join()

    print(f"Squared Sum Worker: {round(time.time() - sum_start_time, 1)}s")

    # I/O-bound workers - sleep with daemon flag
    sleepy_start_time = time.time()
    for i in range(5):
        # daemon=True: thread won't prevent program exit if main finishes
        s = SleepyWorker((i + 1), daemon=True)
        threads.append(s)

    for thread in threads:
        thread.join()

    print(f"Sleepy Worker: {round(time.time() - sleepy_start_time, 1)}s")


if __name__ == "__main__":
    main()