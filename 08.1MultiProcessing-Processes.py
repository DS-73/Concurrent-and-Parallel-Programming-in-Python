import os
import time
from multiprocessing import Process


def check_value_in_list(x):
    print("Child PID:", os.getpid())
    print("Parent PID:", os.getppid())
    for i in range(10**8):
        i in x


num_threads = 4
comparision_list = [1,2,3,4]

start_time = time.time()
threads = []
for i in range(num_threads):
    t = Process(target=check_value_in_list, args=(comparision_list,))
    threads.append(t)

if __name__ == "__main__":
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Total time elapsed: {time.time() - start_time} seconds")