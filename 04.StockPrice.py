from Workers.WikiWorker import WikiWorker
from Workers.YahooFinance import YahooFinance

wikiWorker = WikiWorker()
prices = []

print("Processing S&P")
print("=" * 50)
for symbol in wikiWorker.get_snp_500_companies():
    y = YahooFinance(symbol)
    prices.append(y)

if len(prices) > 0:
    print("Symbols aquired ")
    print("=" * 50)

    for stock in prices:
        stock.join()