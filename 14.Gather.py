"""
Asyncio Concurrent Execution with gather()

This module demonstrates asyncio.gather() for running multiple
coroutines concurrently and collecting their results.

Purpose:
    - Show asyncio.gather() for concurrent execution
    - Demonstrate passing arguments to coroutines
    - Measure elapsed time for concurrent vs sequential

Key Insight:
    gather() schedules all coroutines concurrently and waits for all.
    Total time ≈ slowest coroutine (not sum).

Concepts:
    - asyncio.gather(*coroutines): Run concurrently, return list of results
    - Preserves order of results matching input order
    - Exceptions: first exception raised unless return_exceptions=True
"""

import asyncio
import time


async def async_sleep(n: int) -> None:
    """
    Asynchronous sleep coroutine with identifier.

    Args:
        n: Identifier for this sleep instance (for logging).
    """
    print(" >> Async Sleep: Begin", n)
    await asyncio.sleep(3)
    print(" >> Async Sleep: End", n)


async def main() -> None:
    """
    Run three sleep coroutines concurrently using gather().

    All three 3-second sleeps run simultaneously.
    Expected elapsed time: ~3 seconds (not 9).
    """
    begin = time.time()

    # gather() runs all coroutines concurrently
    await asyncio.gather(
        async_sleep(1),
        async_sleep(2),
        async_sleep(3)
    )

    print(f"Time Elapsed: {(time.time() - begin):.3f}")


if __name__ == "__main__":
    asyncio.run(main())