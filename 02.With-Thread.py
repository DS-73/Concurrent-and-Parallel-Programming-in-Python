import time
import threading


def calculate_sum_squares(n: int) -> int:
    sum_squares = 0
    for i in range(n):
        sum_squares += i ** 2

    print(sum_squares)


def sleep_a_little(seconds: int):
    time.sleep(seconds)


def main():
    square_time_start = time.time()
    current_threads = []

    for i in range(5):
        t = threading.Thread(
            target=calculate_sum_squares,
            args=((i + 1) * 1000000,)
        )
        t.start()
        current_threads.append(t)

    for x in current_threads:
        x.join()

    print(f"Sum of Squares Task: {round(time.time() - square_time_start, 1)}")

    sleep_time_start = time.time()
    for i in range(1, 6):
        t = threading.Thread(
            target=sleep_a_little,
            args=(i,)
        )
        t.start()
        current_threads.append(t)

    for x in current_threads:
        x.join()

    print(f"Sleeping Task: {round(time.time() - sleep_time_start, 1)}")


if __name__ == "__main__":
    main()