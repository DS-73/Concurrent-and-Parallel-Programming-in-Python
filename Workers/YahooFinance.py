import threading

import requests
from lxml import html


class YahooFinance(threading.Thread):
    __baseurl = "https://finance.yahoo.com/quote/"

    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)
        self._symbol = symbol
        self.headers = {
            "User-Agent": f"{self._symbol}/1.0 (https://{self._symbol}.com/contact; {self._symbol}@{self._symbol}.com)"
        }
        self.start()

    def run(self):
        url = f"{YahooFinance.__baseurl}{self._symbol}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
        except requests.RequestException as e:
            print(f"Error fetching {self._symbol}: {e}")
            return

        if response.status_code != 200:
            print(f"Error: {self._symbol} not available! {response.status_code}")
            return
            
        text = html.fromstring(response.text)
        price_elements = text.xpath("/html/body/div/div[4]/main/section/section/section/section/section[1]/div[2]/div[1]/section/div/section/div[1]/span[1]")

        if price_elements:
            print(f"{self._symbol} is at ${price_elements[0].text}")
        else:
            print(f"Could not parse price for {self._symbol}")
