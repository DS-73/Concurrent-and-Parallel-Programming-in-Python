"""
WikiWorker - Wikipedia S&P 500 Scraper

Fetches and parses the list of S&P 500 companies from Wikipedia.
Used as the data source for stock price pipeline.

Purpose:
    - Demonstrate web scraping with requests and BeautifulSoup
    - Provide generator-based symbol iteration
    - Handle HTTP errors gracefully

Dependencies:
    - requests: HTTP client
    - beautifulsoup4: HTML parsing
    - lxml: Parser backend (faster than html.parser)
"""

import requests
from bs4 import BeautifulSoup

# Polite User-Agent identifying our bot
HEADERS = {
    "User-Agent": "MyWikimediaBot/1.0 (https://example.com/contact; you@example.com)"
}


class WikiWorker:
    """
    Scrapes S&P 500 company symbols from Wikipedia.

    Fetches the List of S&P 500 companies page and extracts
    ticker symbols from the constituents table.

    Attributes:
        _url: Wikipedia page URL for S&P 500 list.
    """

    def __init__(self) -> None:
        """Initialize with Wikipedia S&P 500 page URL."""
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def _extract_company_symbols(self, response: requests.Response):
        """
        Parse HTML response and yield company symbols.

        Args:
            response: requests.Response from Wikipedia page.

        Yields:
            str: Stock ticker symbol for each S&P 500 company.
        """
        soup = BeautifulSoup(response.text, "lxml")

        # Find the constituents table by ID
        table = soup.find(id="constituents")
        if not table:
            return

        table_rows = table.find_all("tr")

        # Skip header row (index 0), process data rows
        for row in table_rows[1:]:
            # First td contains the symbol
            symbol_cell = row.find("td")
            if symbol_cell:
                yield symbol_cell.text.strip()

    def get_snp_500_companies(self):
        """
        Fetch Wikipedia page and yield S&P 500 symbols.

        Returns:
            Generator yielding ticker symbols.

        Yields:
            str: Stock symbol for each company in the index.

        Note:
            Returns empty generator on HTTP error (prints error message).
        """
        try:
            response = requests.get(self._url, headers=HEADERS, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching Wikipedia: {e}")
            return

        yield from self._extract_company_symbols(response)