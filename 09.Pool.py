"""
Process Pool vs Thread Pool Comparison

This module compares multiprocessing.Pool (process-based) vs
threading.Thread (thread-based) for CPU-bound work.

Purpose:
    - Demonstrate Pool.map() for easy parallel execution
    - Compare process pool vs thread performance for CPU-bound tasks
    - Show cpu_count() for optimal worker count

Concept:
    - Pool manages a fixed number of worker processes
    - map() distributes iterable items across workers
    - Processes bypass GIL; threads don't for CPU-bound work
"""

import time
from multiprocessing import Pool, cpu_count
from threading import Thread


# Use all but one CPU to keep system responsive
NUM_PROCESSES = max(1, cpu_count() - 1)
ITEM_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def squared(x: int) -> int:
    """
    CPU-bound function: busy loop simulating computation.

    Args:
        x: Input value (unused, just for interface compatibility).

    Returns:
        The input value (result not used, focus is on timing).
    """
    for _ in range(10**8):
        pass
    return x


def run_process_pool() -> float:
    """
    Execute squared() across items using process pool.

    Returns:
        Elapsed time in seconds.
    """
    start = time.time()
    with Pool(NUM_PROCESSES) as pool:
        pool.map(squared, ITEM_LIST)
    return time.time() - start


def run_thread_pool() -> float:
    """
    Execute squared() across items using threads.

    Returns:
        Elapsed time in seconds.
    """
    threads = [Thread(target=squared, args=(item,)) for item in ITEM_LIST]
    start = time.time()

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return time.time() - start


def main() -> None:
    """Run both approaches and compare timings."""
    print(f"Total available CPUs: {cpu_count()}")
    print(f"Using {NUM_PROCESSES} processes")

    process_time = run_process_pool()
    print(f"Process Pool time elapsed: {process_time:.3f} seconds")

    thread_time = run_thread_pool()
    print(f"Thread time elapsed: {thread_time:.3f} seconds")

    print(f"\nSpeedup (process/thread): {thread_time/process_time:.2f}x")


if __name__ == "__main__":
    main()