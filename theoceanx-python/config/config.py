# from dotenv import DotEnv
import copy


class Config:
    # TODO env = DotEnv('.env')

    default_config = {
        'web3Provider': 'http://localhost:8545',
        'websockets': 'https://dev-ws.theoceanx.com:443',  # TODO Between process type
        'api': {
            'BASE_URL': 'https://kovan.theoceanx.com/api/v0',  # env.get('BASE_URL'),   TODO Between process type
            'ORDER': '/order',
            'TOKEN_PAIRS': '/token_pairs',
            'ORDER_BOOK': '/order_book',
            'CANCEL_ORDER': '/cancel_order',
            'RESERVE_MARKET_ORDER': '/market_order/reserve',
            'PLACE_MARKET_ORDER': '/market_order/place',
            'RESERVE_LIMIT_ORDER': '/limit_order/reserve',
            'PLACE_LIMIT_ORDER': '/limit_order/place',
            'USER_HISTORY': '/user_history',
            'TICKER': '/ticker',
            'TICKERS': '/tickers',
            'CANDLESTICKS': '/candlesticks',
            'CANDLESTICKS_INTERVALS': '/candlesticks/intervals',
            'TRADE_HISTORY': '/trade_history',
            'ORDER_INFO': '/order',
            'AUTH_TOKENS': '/auth/token',
            'AUTH_REFRESH': '/auth/refresh',
            'AVAILABLE_BALANCE': '/available_balance'
        },
        'relay': {
            'funnel': '0x00ba938cc0df182c25108d7bf2ee3d37bce07513',
            'feeRecipient': '0x88a64b5e882e5ad851bea5e7a3c8ba7c523fecbe'
        }
    }

    config = copy.deepcopy(default_config)

    def set_config(self, c):
        self.config = self.default_config.update(c)

    def get_config(self):
        return self.config

    def update_config_exchange(self, zero_ex):
        c = self.get_config()

        if c['relay']['exchange']:
            c['relay']['exchange'] = zero_ex.exchange.getContractAddress()

        self.set_config(c)
