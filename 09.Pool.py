import time
from multiprocessing import Pool, cpu_count
from threading import Thread

num_processes = max(1, cpu_count() - 1)
item_list = [1,2,3,4,5,6,7,8,9]

def squared(x):
    for i in range(10 ** 8):
        pass

if __name__ == "__main__":
    print(f"Total available CPUs: {num_processes}")
    start_process = time.time()
    with Pool(num_processes) as pool:
        result = pool.map(squared, item_list)

    print(f"Process Pool time elapsed: {(time.time() - start_process):.3f} seconds")

    threads = [Thread(target=squared, args=(item_list[_],)) for _ in range(len(item_list))]
    start_thread = time.time()
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Thread time elapsed: {(time.time() - start_thread):.3f} seconds")
    