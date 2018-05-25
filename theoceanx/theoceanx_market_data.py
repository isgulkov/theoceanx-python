from .api.market_api import MarketAPI

class MarketData:
    market = MarketAPI()

    def token_pairs(self):
        return self.market.get_tickers()  # TODO: not implemented -- returns None

m = MarketData()

print(m.token_pairs())
