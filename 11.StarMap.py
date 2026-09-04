"""
Pool.starmap for Multiple Arguments

This module demonstrates Pool.starmap() for parallel execution
of functions requiring multiple arguments.

Purpose:
    - Show starmap() as alternative to partial() for multi-arg functions
    - Demonstrate zipping iterables for parallel argument passing
    - Compare with partial approach (10.Partial.py)

Concept:
    starmap(func, iterable) expects iterable of tuples,
    unpacking each tuple as func(*tuple). More flexible than partial.
"""

from multiprocessing import Pool, cpu_count


def squared(x: int, y: int) -> int:
    """
    Compute x raised to power y.

    Args:
        x: Base value.
        y: Exponent.

    Returns:
        x ** y
    """
    return x ** y


def main() -> None:
    """Execute parallel power computation with varying bases and exponents."""
    my_list = [1, 2, 3, 4, 5, 6]
    power_list = [1, 2, 3, 4, 5, 6]

    max_processes = max(1, cpu_count() - 1)

    with Pool(max_processes) as pool:
        # zip creates tuples: (1,1), (2,2), (3,3), ...
        # starmap unpacks: squared(1,1), squared(2,2), ...
        results = pool.starmap(squared, zip(my_list, power_list))

        # Alternative: list comprehension to create tuples
        # results = pool.starmap(squared, [(my_list[i], power_list[i]) for i in range(len(my_list))])

    # Expected: [1^1, 2^2, 3^3, 4^4, 5^5, 6^6]
    #           = [1, 4, 27, 256, 3125, 46656]
    print(f"Results: {results}")


if __name__ == "__main__":
    main()