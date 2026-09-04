"""
YahooFinance - Stock Price Fetcher Thread

Fetches real-time stock prices from Yahoo Finance using web scraping.
Implements rate limiting, retries, and realistic headers to avoid blocking.

Purpose:
    - Demonstrate threaded web scraping with rate limiting
    - Show Semaphore for concurrent request throttling
    - Implement exponential backoff retry logic
    - Parse dynamic HTML with lxml XPath

Architecture:
    - Class-level Semaphore limits concurrent requests (max 10)
    - Realistic browser headers to avoid bot detection
    - Retry with exponential backoff for rate limits/server errors
    - XPath-based price extraction from Yahoo Finance quote page

Thread Safety:
    - Semaphore shared across all instances (class variable)
    - Each instance stores result in instance variables
    - No shared mutable state between threads

Dependencies:
    - requests: HTTP client
    - lxml: HTML parsing with XPath support
"""

import threading
import time
from datetime import datetime, timezone
import requests
from lxml import html


class YahooFinance(threading.Thread):
    """
    Thread that fetches current stock price from Yahoo Finance.

    Auto-starts on creation. Result stored in _price and _extracted_time.
    Uses class-level semaphore to limit concurrent requests.

    Attributes:
        _symbol: Stock ticker symbol.
        _price: Fetched price (None until complete).
        _extracted_time: UTC timestamp of fetch.
    """

    # Base URL for Yahoo Finance quote pages
    __BASE_URL = "https://finance.yahoo.com/quote/"

    # Limit concurrent requests to avoid rate limiting
    _THROTTLE = threading.Semaphore(10)

    # Realistic browser headers
    __HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, symbol: str, **kwargs) -> None:
        """
        Initialize and start price fetcher for given symbol.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL').
            **kwargs: Passed to Thread.__init__.
        """
        super().__init__(**kwargs)
        self._symbol = symbol
        self._price: float | None = None
        self._extracted_time: datetime | None = None
        self.start()  # Begin fetching immediately

    def _fetch(self, url: str) -> requests.Response | None:
        """
        Fetch URL with retries and exponential backoff.

        Acquires semaphore before each request to respect rate limits.
        Retries on 429 (rate limit) and 503 (service unavailable).

        Args:
            url: Full URL to fetch.

        Returns:
            Response object or None if all retries failed.
        """
        for attempt in range(3):
            try:
                # Limit concurrent requests
                with YahooFinance._THROTTLE:
                    response = requests.get(
                        url,
                        headers=YahooFinance.__HEADERS,
                        timeout=30
                    )

                # Retry on rate limiting or server errors
                if response.status_code in (429, 503):
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue

                return response

            except requests.RequestException:
                time.sleep(2 ** attempt)

        return None

    def run(self) -> None:
        """
        Thread entry point: fetch and parse stock price.

        1. Construct Yahoo Finance URL for symbol
        2. Fetch with retries and throttling
        3. Parse HTML with lxml XPath
        4. Extract price and timestamp
        5. Store in instance variables
        """
        url = f"{YahooFinance.__BASE_URL}{self._symbol}"
        response = self._fetch(url)

        if response is None or response.status_code != 200:
            print(f"Error: {self._symbol} not available!")
            return

        try:
            tree = html.fromstring(response.text)

            # XPath to price element (may need updates if Yahoo changes layout)
            price_elements = tree.xpath(
                "/html/body/div/div[4]/main/section/section/section/section/section[1]"
                "/div[2]/div[1]/section/div/section/div[1]/span[1]"
            )

            if not price_elements:
                raise ValueError(f"No price element found for {self._symbol}")

            # Parse price (remove commas, convert to float)
            price_text = price_elements[0].text.replace(",", "").strip()
            self._price = float(price_text)
            self._extracted_time = datetime.now(timezone.utc)

        except (AttributeError, IndexError, TypeError, ValueError) as e:
            print(f"Could not parse price for {self._symbol}: {e}")

    @property
    def price(self) -> float | None:
        """Get fetched price (None if not yet available)."""
        return self._price

    @property
    def extracted_time(self) -> datetime | None:
        """Get fetch timestamp (None if not yet available)."""
        return self._extracted_time

    @property
    def symbol(self) -> str:
        """Get stock symbol."""
        return self._symbol