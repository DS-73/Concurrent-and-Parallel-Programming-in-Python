"""
Asyncio Basic Example

This module demonstrates the fundamentals of Python's asyncio library
for asynchronous programming with coroutines.

Purpose:
    - Show basic async/await syntax
    - Demonstrate asyncio.run() for executing coroutines
    - Illustrate non-blocking sleep with asyncio.sleep()

Concepts:
    - async def: Defines a coroutine function
    - await: Pauses coroutine until awaitable completes
    - asyncio.run(): Runs the event loop until coroutine finishes
    - asyncio.sleep(): Non-blocking sleep (yields control to event loop)
"""

import asyncio


async def async_sleep() -> None:
    """
    Asynchronous sleep coroutine.

    Prints begin/end messages with a 3-second non-blocking delay.
    During the await, the event loop can run other coroutines.
    """
    print(" >> Async Sleep: Begin")
    await asyncio.sleep(3)
    print(" >> Async Sleep: End")


def main() -> None:
    """
    Execute the async sleep coroutine.

    asyncio.run() creates a new event loop, runs the coroutine,
    and closes the loop. This is the main entry point for asyncio programs.
    """
    print(" >> Main: Begin")
    asyncio.run(async_sleep())
    print(" >> Main: End")


if __name__ == "__main__":
    main()