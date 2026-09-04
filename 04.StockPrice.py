"""
Stock Price Scraper - Sequential Version

This module fetches S&P 500 company symbols from Wikipedia and retrieves
their current stock prices from Yahoo Finance sequentially.

Purpose:
    - Demonstrate web scraping with requests and BeautifulSoup
    - Show sequential price fetching (slow, for comparison)
    - Foundation for concurrent versions in later examples

Dependencies:
    - requests: HTTP library
    - beautifulsoup4: HTML parsing
    - lxml: Parser backend for BeautifulSoup
    - Workers.WikiWorker: Wikipedia S&P 500 scraper
    - Workers.YahooFinance: Yahoo Finance price fetcher (threaded)
"""

import time
from Workers.WikiWorker import WikiWorker
from Workers.YahooFinance import YahooFinance


def main() -> None:
    """
    Sequentially fetch stock prices for all S&P 500 companies.

    Process:
    1. WikiWorker scrapes S&P 500 symbols from Wikipedia
    2. For each symbol, create YahooFinance thread to fetch price
    3. Stagger launches with sleep to avoid rate limiting
    4. Wait for all threads to complete with join()

    Note: YahooFinance threads run concurrently, but launched sequentially
    with delays. This is a hybrid approach.
    """
    wiki_worker = WikiWorker()
    price_threads = []

    print("Processing S&P 500")
    print("=" * 50)

    # Launch price fetchers for each symbol
    for symbol in wiki_worker.get_snp_500_companies():
        y = YahooFinance(symbol)
        price_threads.append(y)
        time.sleep(0.1)  # Stagger launches to avoid Yahoo rate limiting

    if len(price_threads) > 0:
        print("Symbols acquired")
        print("=" * 50)

        # Wait for all price fetchers to complete
        for stock in price_threads:
            stock.join()


if __name__ == "__main__":
    main()