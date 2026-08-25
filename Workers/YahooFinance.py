import threading
import time
from datetime import datetime, timezone
import requests
from lxml import html


class YahooFinance(threading.Thread):
    __baseurl = "https://finance.yahoo.com/quote/"

    # Cap how many requests hit Yahoo at the same time to avoid being blocked
    _throttle = threading.Semaphore(10)

    # Realistic browser headers so Yahoo does not treat us as a bot
    __headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)
        self._symbol = symbol
        self._price = None
        self._extracted_time = None
        self.start()

    def _fetch(self, url):
        """Fetch the URL with retries and exponential backoff."""
        for attempt in range(3):
            try:
                with YahooFinance._throttle:
                    response = requests.get(url, headers=YahooFinance.__headers, timeout=30)

                # Retry on rate limiting / server errors
                if response.status_code in (429, 503):
                    time.sleep(2 ** attempt)
                    continue
                return response
            except requests.RequestException:
                time.sleep(2 ** attempt)
        return None

    def run(self):
        url = f"{YahooFinance.__baseurl}{self._symbol}"
        response = self._fetch(url)

        if response is None or response.status_code != 200:
            print(f"Error: {self._symbol} not available!")
            return

        try:
            text = html.fromstring(response.text)
            price_elements = text.xpath("/html/body/div/div[4]/main/section/section/section/section/section[1]/div[2]/div[1]/section/div/section/div[1]/span[1]")

            if not price_elements:
                raise ValueError(f"No price element found for {self._symbol}")

            self._price = float(price_elements[0].text.replace(",", "").strip())
            self._extracted_time = datetime.now(timezone.utc)

        except (AttributeError, IndexError, TypeError, ValueError):
            print(f"Could not parse price for {self._symbol}")
