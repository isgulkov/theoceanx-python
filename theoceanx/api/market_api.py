# from ..config import get_config
import pprint
import asyncio
import types
from aiohttp import ClientSession


class MarketAPI:
    BASE_URL = 'https://kovan.theoceanx.com/api/v0'
    HEADERS = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    def get_pairs(self):
        """Return all tradeable token pairs on The Ocean X."""

        return self._request('/token_pairs')

    def get_ticker(self, base_token_address, quote_token_address):
        """Return 24 hour trading activity for a token pair.
        
        Keyword arguments:
        base_token_address -- Base token address
        quote_token_address -- Quote token address
        """

        pass

    def get_tickers(self):
        """Return 24 hour trading activity for all token pairs."""

        pass

    def get_order_book(self):
        """Return the current order book for a token pair."""

        pass

    def get_trade_history(self):
        """Retrieves the last 100 trades for a given token pair."""

        pass

    def get_candlesticks(self):
        """Return historical candlestick data."""

        pass

    def get_candlesticks_intervals(self):
        """Return all available candlesticks intervals."""

        pass

    def get_order_info(self):
        """Return additional order information."""

        pass

    def get_available_balance(self):
        """Return token balance."""

        pass

    # def req_wrapper(self, f, arg_func, ):


    # qs = {'key1': 'value1', 'key2': 'value2'} GET Parameters
    async def _request(self, path, qs={}, payload=''):
        url = self.BASE_URL + path

        async with ClientSession() as session:
            async with session.get(url, headers=self.HEADERS, params=qs, data=payload) as r:
                r = await r.read()
                print(r)


m = MarketAPI()

token_pair = m.get_pairs()

loop = asyncio.get_event_loop()
loop.run_until_complete(token_pair)
