from functools import partial
from multiprocessing import Pool, cpu_count


def squared(y, addition_comp, x):
    return x ** y + addition_comp


if __name__ == "__main__":
    power, addition_component = 2, 10
    
    partial_func = partial(squared, power, addition_component)

    my_list = [1,2,3,4,5,6]
    max_processes = max(1, cpu_count() - 5)

    with Pool() as p:
        res = p.map(partial_func, my_list)

    print(res)
    