import asyncio
import time


async def async_sleep(n):
    n = max(2, n)
    for i in range(1, n):
        yield i
        await asyncio.sleep(i)


async def main():
    s = time.time()
    async for x in async_sleep(5):
          print(x)

    print(f"Time Elapsed: {time.time() - s}")

if __name__ == "__main__":
    asyncio.run(main())