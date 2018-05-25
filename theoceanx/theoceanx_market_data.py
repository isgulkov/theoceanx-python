from .api import market_api as market

class MarketData:
    def token_pairs(self):
        return market.get_tickers()

m = MarketData()

print(m.token_pairs())
