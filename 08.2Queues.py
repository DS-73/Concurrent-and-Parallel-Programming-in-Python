"""
Inter-Process Communication with Queues

This module demonstrates using multiprocessing.Queue for
thread-safe data exchange between processes.

Purpose:
    - Show Queue for producer-consumer pattern across processes
    - Demonstrate work distribution (data partitioning) among processes
    - Illustrate sentinel pattern for graceful shutdown

Architecture:
    - Main process: Creates queue, spawns workers, collects results
    - Worker processes: Each processes a partition of the data range
    - Queue: Thread-safe FIFO for returning results to main process

Work Distribution:
    Total range: 0 to 10^9 - 1
    Divided evenly among N processes
    Each process checks membership for its partition
"""

import os
import time
from multiprocessing import Process, Queue


def check_value_in_list(
    x: list,
    partition_index: int,
    num_partitions: int,
    queue: Queue
) -> None:
    """
    Process a partition of the search range and return hit count.

    Args:
        x: List to check membership against.
        partition_index: This worker's partition number (0-based).
        num_partitions: Total number of partitions.
        queue: Queue to put result tuple (start, end, hit_count).
    """
    # Calculate this partition's range
    start = (partition_index * 10**9) // num_partitions
    end = ((partition_index + 1) * 10**9) // num_partitions

    hit_count = 0
    for i in range(start, end):
        if i in x:
            hit_count += 1

    # Send result back to main process
    queue.put((start, end, hit_count))


def main() -> None:
    """Run parallel search with work partitioning and result collection."""
    num_processes = 4
    comparison_list = [1, 2, 3, 4]

    start_time = time.time()
    processes = []
    queue = Queue()

    # Spawn worker processes
    for i in range(num_processes):
        p = Process(
            target=check_value_in_list,
            args=(comparison_list, i, num_processes, queue)
        )
        processes.append(p)

    # Start all workers
    for p in processes:
        p.start()

    # Wait for all to complete
    for p in processes:
        p.join()

    # Sentinel to signal end of results
    queue.put("Done")

    # Collect and print results
    while True:
        val = queue.get()
        if val == "Done":
            break
        print(f"Range {val[0]} - {val[1]}: {val[2]} hits")

    print(f"Total time elapsed: {time.time() - start_time:.3f} seconds")


if __name__ == "__main__":
    main()