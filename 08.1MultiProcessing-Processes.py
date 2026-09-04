"""
Multiprocessing for CPU-Bound Parallelism

This module demonstrates true parallelism for CPU-bound tasks
using Python's multiprocessing module (bypasses GIL).

Purpose:
    - Show multiprocessing.Process for CPU-bound work
    - Compare with threading version (08.0MultiProcessing-Threads.py)
    - Demonstrate process creation, PID tracking, and timing

Concept:
    Each Process has its own Python interpreter and memory space,
    so each has its own GIL. True parallel execution on multi-core CPUs.

Task:
    Same as threading version: 100 million membership checks per process.
"""

import os
import time
from multiprocessing import Process


def check_value_in_list(x: list) -> None:
    """
    Perform CPU-bound membership checks in a separate process.

    Prints process IDs to demonstrate separate memory spaces.

    Args:
        x: List to check membership against (copied to each process).
    """
    print(f"Child PID: {os.getpid()}")
    print(f"Parent PID: {os.getppid()}")
    for i in range(10**8):
        i in x


def main() -> None:
    """Run CPU-bound task with multiple processes and measure time."""
    num_processes = 4
    comparison_list = [1, 2, 3, 4]

    start_time = time.time()
    processes = []

    # Create processes (not started yet)
    for _ in range(num_processes):
        p = Process(target=check_value_in_list, args=(comparison_list,))
        processes.append(p)

    # Start all processes
    for p in processes:
        p.start()

    # Wait for completion
    for p in processes:
        p.join()

    print(f"Total time elapsed: {time.time() - start_time:.3f} seconds")


if __name__ == "__main__":
    # Required for multiprocessing on Windows/macOS (spawn method)
    main()