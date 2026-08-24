import time


def calculate_sum_squares(n: int) -> int:
    """Calculate and print the sum of squares from 0 to n-1."""
    sum_squares = 0
    for i in range(n):
        sum_squares += i ** 2

    print(sum_squares)


def sleep_a_little(seconds: int):
    """Sleep for the specified number of seconds."""
    time.sleep(seconds)


def main():
    """Run sequential tasks: calculate sum of squares and sleep delays."""
    square_time_start = time.time()
    for i in range(5):
        calculate_sum_squares((i + 1) * 1000000)

    print(f"Sum of Squares Task: {round(time.time() - square_time_start, 1)}")

    sleep_time_start = time.time()
    for i in range(1, 6):
        sleep_a_little(i)

    print(f"Sleeping Task: {round(time.time() - sleep_time_start, 1)}")


if __name__ == "__main__":
    main()