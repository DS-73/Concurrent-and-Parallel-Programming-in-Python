"""
Stock Price Pipeline with PostgreSQL Storage

This module implements a complete pipeline: scrape S&P 500 symbols,
fetch prices from Yahoo Finance concurrently, and store in PostgreSQL.

Architecture:
    1. WikiWorker -> scrapes symbols from Wikipedia (producer)
    2. YahooFinance threads -> fetch prices concurrently (workers)
    3. PostgresMasterScheduler threads -> consume price queue, insert to DB (consumers)

Purpose:
    - Demonstrate producer-consumer pattern with queues
    - Show thread-safe queue communication between workers
    - Implement complete ETL pipeline with concurrent stages

Dependencies:
    - multiprocessing.Queue: Thread-safe queue for inter-thread communication
    - Workers.WikiWorker: Symbol scraper
    - Workers.YahooFinance: Price fetcher (threaded with semaphore)
    - Workers.PostgresWorker: Database writer (PostgresMasterScheduler + PostgresWorker)
"""

import time
from multiprocessing import Queue

from Workers.PostgresWorker import PostgresMasterScheduler, PostgresWorker
from Workers.WikiWorker import WikiWorker
from Workers.YahooFinance import YahooFinance


def main() -> None:
    """
    Execute the complete stock price scraping and storage pipeline.

    Pipeline stages:
    1. Scrape S&P 500 symbols from Wikipedia
    2. Launch YahooFinance threads for each symbol (with rate limiting)
    3. Collect results into a thread-safe queue
    4. Launch PostgresMasterScheduler workers to consume queue and insert to DB
    5. Send sentinel values (None) to gracefully shut down workers
    6. Verify by reading back from database
    """
    wiki_worker = WikiWorker()

    print("=== Processing stock price information ===")
    finance_threads = []

    # Stage 1: Launch price fetchers for all symbols
    for symbol in wiki_worker.get_snp_500_companies():
        yahoo_finance = YahooFinance(symbol)
        finance_threads.append(yahoo_finance)
        time.sleep(0.1)  # Stagger to respect Yahoo rate limits

    # Stage 2: Thread-safe queue for passing data to DB workers
    postgres_queue: Queue = Queue()

    # Wait for all price fetchers and populate queue
    for finance_thread in finance_threads:
        finance_thread.join()
        if finance_thread._price:
            postgres_queue.put((
                finance_thread._symbol,
                finance_thread._price,
                finance_thread._extracted_time
            ))

    print("=== Price information processed ===")

    # Stage 3: Launch database writer workers
    postgres_scheduler_threads = []
    num_postgres_workers = 2

    print("=== Updating Database ===")
    for _ in range(num_postgres_workers):
        scheduler = PostgresMasterScheduler(postgres_queue)
        postgres_scheduler_threads.append(scheduler)

    # Stage 4: Send sentinel (None) per worker for graceful shutdown
    for _ in range(num_postgres_workers):
        postgres_queue.put(None)

    # Wait for all DB workers to finish
    for pst in postgres_scheduler_threads:
        pst.join()

    print("=== Database update complete ===")

    # Stage 5: Verify by reading back
    postgres_worker = PostgresWorker("TEST", 1.0, "2024-01-01")
    postgres_worker._select_from_db()


if __name__ == "__main__":
    main()