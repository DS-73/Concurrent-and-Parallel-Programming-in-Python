"""
Thread Synchronization with Locks

This module demonstrates thread-safe counter increment using
threading.Lock to prevent race conditions.

Purpose:
    - Show race condition problem with shared mutable state
    - Demonstrate Lock usage for mutual exclusion
    - Verify correct final count with proper synchronization

Concept:
    Without lock: Multiple threads read/write 'counter' simultaneously,
    causing lost updates. With lock: Only one thread can increment at a time.
"""

import threading

# Shared counter - accessed by all threads
counter = 0

# Lock for mutual exclusion - ensures atomic increment
lock = threading.Lock()


def increment() -> None:
    """
    Increment global counter 10 million times with lock protection.

    The 'with lock:' context manager ensures:
    - Lock acquired before entering block
    - Lock released after block (even if exception)
    - Only one thread executes the critical section at a time
    """
    global counter
    for _ in range(10**7):
        with lock:
            counter += 1


def main() -> None:
    """Create and run 4 threads that increment the shared counter."""
    threads: list[threading.Thread] = []

    # Create 4 worker threads
    for _ in range(4):
        t = threading.Thread(target=increment)
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all to complete
    for t in threads:
        t.join()

    # Expected: 4 * 10,000,000 = 40,000,000
    # Without lock: would be less due to race conditions
    print(f"Final counter value: {counter}")


if __name__ == "__main__":
    main()