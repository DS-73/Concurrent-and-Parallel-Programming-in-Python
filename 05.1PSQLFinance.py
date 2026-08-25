import time
from multiprocessing import Queue

from Workers.PostgresWorker import PostgresMasterScheduler, PostgresWorker
from Workers.WikiWorker import WikiWorker
from Workers.YahooFinance import YahooFinance


def main():
    wikiWorker = WikiWorker()

    print("=== Processing stock price information === ")
    finance_queue = []
    for symbol in wikiWorker.get_snp_500_companies():
        yahooFinance = YahooFinance(symbol)    
        finance_queue.append(yahooFinance)
        time.sleep(0.1)

    postgres_queue = Queue()
    
    for finance_thread in finance_queue:
        finance_thread.join()
        if finance_thread._price:
            postgres_queue.put((finance_thread._symbol, finance_thread._price, finance_thread._extracted_time))

    print("=== Price information processed === ")

    postgres_scheduler_threads = []
    num_postgres_workers = 2

    print("=== Updating Database === ")
    for i in range(num_postgres_workers):
        postgresMasterScheduler = PostgresMasterScheduler(postgres_queue)
        postgres_scheduler_threads.append(postgresMasterScheduler)

    # One None sentinel per worker so each scheduler can exit its loop
    for _ in range(num_postgres_workers):
        postgres_queue.put(None)

    for pst in postgres_scheduler_threads:
        pst.join()

    print("=== Database update complete ===")

    postgres_worker = PostgresWorker(1,2,3)
    postgres_worker._select_from_db()
    

if __name__ == "__main__":
    main()