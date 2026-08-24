import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "MyWikimediaBot/1.0 (https://example.com/contact; you@example.com)"
}

class WikiWorker:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def _extract_company_symbols(self, response):
        text = BeautifulSoup(response.text, "lxml")

        table = text.find(id="constituents")
        table_rows = table.find_all('tr')

        for row in table_rows[1:]:
            yield row.find("td").text.strip()

    def get_snp_500_companies(self):
        response = requests.get(self._url, headers=headers, timeout=30)
        if response.status_code != 200:
            print("Error: Connection issue !!!")
            return []
        
        yield from self._extract_company_symbols(response)
