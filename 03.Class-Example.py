import time
from Workers.SleepyWorker import SleepyWorker
from Workers.SquaredSumWorker import SquaredSumWorker


def main():
    """Run threaded worker examples: squared sum and sleepy workers."""
    sum_start_time = time.time()
    threads = []

    for i in range(5):
        s = SquaredSumWorker((i + 1) * 1000000)
        threads.append(s)

    for thread in threads:
        thread.join()

    print(f"Squared Sum Worker: {round(time.time() - sum_start_time, 1)}")

    sleepy_start_time = time.time()
    for i in range(5):
        s = SleepyWorker((i + 1), daemon=True)
        threads.append(s)

    for thread in threads:
        thread.join()

    print(f"Sleepy Worker: {round(time.time() - sleepy_start_time, 1)}")


if __name__ == "__main__":
    main()