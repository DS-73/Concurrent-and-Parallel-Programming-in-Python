import os
import time
from multiprocessing import Process, Queue

def check_value_in_list(x, s, num, queue):

    hit_count = 0
    start, end = (s * 10**9) // num, ((s + 1) * 10**9) // num
    for i in range(start, end):
        if i in x:
            hit_count += 1

    queue.put((start, end, hit_count))

if __name__ == "__main__":
    num_processes = 4
    comparision_list = [1,2,3,4]

    start_time = time.time()
    processes = []

    queue = Queue()
    for i in range(num_processes):
        t = Process(target=check_value_in_list, args=(comparision_list, i, num_processes, queue))
        processes.append(t)

    for t in processes:
        t.start()
    for t in processes:
        t.join()

    queue.put("Done")

    while True:
        val = queue.get()
        if val == "Done":
            break
        print(val)


    print(f"Total time elapsed: {time.time() - start_time} seconds")