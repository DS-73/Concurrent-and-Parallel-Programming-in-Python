"""
functools.partial with Process Pool

This module demonstrates using functools.partial to fix
function arguments for use with Pool.map().

Purpose:
    - Show how partial() binds arguments to create callable
    - Enable Pool.map() with multi-argument functions
    - Compare with starmap approach (11.StarMap.py)

Concept:
    partial(func, *args, **keywords) returns a new callable
    with some arguments pre-filled. Pool.map() only accepts
    single-argument functions, so partial adapts multi-arg functions.
"""

from functools import partial
from multiprocessing import Pool, cpu_count


def squared(y: int, addition_comp: int, x: int) -> int:
    """
    Compute x^y + addition_comp.

    Args:
        y: Exponent.
        addition_comp: Constant to add.
        x: Base value.

    Returns:
        x raised to power y, plus addition_comp.
    """
    return x ** y + addition_comp


def main() -> None:
    """Execute parallel computation with partially applied function."""
    # Fixed parameters for all calls
    power = 2
    addition_component = 10

    # Create callable with first two args bound
    # Result: partial_func(x) == squared(2, 10, x)
    partial_func = partial(squared, power, addition_component)

    my_list = [1, 2, 3, 4, 5, 6]
    # Use reasonable process count
    max_processes = max(1, cpu_count() - 1)

    with Pool(max_processes) as pool:
        # map passes each list item as the remaining argument
        results = pool.map(partial_func, my_list)

    # Expected: [1^2+10, 2^2+10, 3^2+10, 4^2+10, 5^2+10, 6^2+10]
    #           = [11, 14, 19, 26, 35, 46]
    print(f"Results: {results}")


if __name__ == "__main__":
    main()