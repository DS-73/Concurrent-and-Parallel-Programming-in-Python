"""
Asyncio Sequential vs Concurrent Execution

This module demonstrates the difference between sequential await
and concurrent execution using asyncio.create_task().

Purpose:
    - Show sequential await (one after another)
    - Demonstrate create_task() for concurrent scheduling
    - Measure elapsed time to illustrate the difference

Key Insight:
    Sequential await: Total time = sum of individual times
    create_task(): Both tasks run concurrently, total time ≈ max individual time

Concepts:
    - asyncio.create_task(): Schedule coroutine concurrently, returns Task
    - Task: Future-like object representing scheduled coroutine
    - await task: Wait for task completion
"""

import asyncio
import time


async def async_sleep() -> None:
    """
    Asynchronous sleep coroutine with 3-second delay.

    Simulates an I/O-bound operation (network request, file read, etc.)
    """
    print(" >> Async Sleep: Begin")
    await asyncio.sleep(3)
    print(" >> Async Sleep: End")


async def main() -> None:
    """
    Compare sequential vs concurrent execution timing.

    This version uses SEQUENTIAL await - each sleep runs one after another.
    Expected elapsed time: ~6 seconds (3 + 3)

    To make concurrent, use:
        task1 = asyncio.create_task(async_sleep())
        task2 = asyncio.create_task(async_sleep())
        await task1
        await task2
    """
    begin = time.time()

    # Sequential: each await blocks until complete
    await async_sleep()
    await async_sleep()

    print(f"Time Elapsed: {(time.time() - begin):.3f}")


if __name__ == "__main__":
    asyncio.run(main())