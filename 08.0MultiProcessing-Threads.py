"""
Threading vs CPU-Bound Work: GIL Limitation Demo

This module demonstrates that Python threads don't provide true
parallelism for CPU-bound tasks due to the Global Interpreter Lock (GIL).

Purpose:
    - Show GIL impact on CPU-bound threading
    - Compare with multiprocessing version (08.1MultiProcessing-Processes.py)
    - Illustrate why multiprocessing is needed for CPU-bound parallelism

Task:
    Check if values exist in a list (CPU-bound 'in' operation)
    repeated 100 million times per thread.

Expected:
    Thread version shows minimal speedup over single thread
    due to GIL contention.
"""

import time
from threading import Thread


def check_value_in_list(x: list) -> None:
    """
    Perform CPU-bound membership checks in a loop.

    This operation holds the GIL and doesn't release it,
    preventing true parallel execution across threads.

    Args:
        x: List to check membership against.
    """
    for i in range(10**8):
        i in x


def main() -> None:
    """Run CPU-bound task with multiple threads and measure time."""
    num_threads = 4
    comparison_list = [1, 2, 3, 4]

    start_time = time.time()
    threads = []

    # Create and start threads
    for _ in range(num_threads):
        t = Thread(target=check_value_in_list, args=(comparison_list,))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Total time elapsed: {time.time() - start_time:.3f} seconds")


if __name__ == "__main__":
    main()