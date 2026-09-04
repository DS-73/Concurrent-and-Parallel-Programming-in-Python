from functools import partial
from multiprocessing import Pool, cpu_count


def squared(x, y):
    return x ** y


if __name__ == "__main__":
    power, addition_component = 2, 10

    my_list = [1,2,3,4,5,6]
    power_list = [1,2,3,4,5,6]
    max_processes = max(1, cpu_count() - 5)

    with Pool() as p:
        res = p.starmap(squared, zip(my_list, power_list))
            # OR [(my_list[i], power_list[i]) for i in range(len(my_list))]

    print(res)
    