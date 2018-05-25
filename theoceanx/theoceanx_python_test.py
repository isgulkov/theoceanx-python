import asyncio
import base64
import binascii
import hashlib
import hmac
import json
import time

import requests
from dotenv import DotEnv
from requests import Request, Session
from web3 import HTTPProvider, Web3

env = DotEnv('.env')

BASE_URL = env.get('BASE_URL')  # The Ocean X staging environment
WEB3_URL = env.get('WEB3_URL')  # This is the default for Parity

RESERVE_MARKET_ORDER = BASE_URL + '/market_order/reserve'
PLACE_MARKET_ORDER = BASE_URL + '/market_order/place'
USER_HISTORY = BASE_URL + '/user_history'

API_KEY = env.get('API_KEY')
API_SECRET = env.get('API_SECRET')
ETHEREUM_ADDRESS = env.get('ETHEREUM_ADDRESS')

print(API_KEY, API_SECRET, ETHEREUM_ADDRESS)

web3 = Web3(HTTPProvider(WEB3_URL))


def sign_order(order):
    signed_order = order
    signed_order['maker'] = ETHEREUM_ADDRESS
    values = [
        Web3.toChecksumAddress(signed_order['exchange_contract_address']),
        Web3.toChecksumAddress(signed_order['maker']),
        Web3.toChecksumAddress(signed_order['taker']),
        Web3.toChecksumAddress(signed_order['maker_token_address']),
        Web3.toChecksumAddress(signed_order['taker_token_address']),
        Web3.toChecksumAddress(signed_order['fee_recipient']),

        int(signed_order['maker_token_amount']),
        int(signed_order['taker_token_amount']),
        int(signed_order['maker_fee']),
        int(signed_order['taker_fee']),
        int(signed_order['expiration_unix_timestamp_sec']),
        int(signed_order['salt'])
    ]
    types = [
        'address',
        'address',
        'address',
        'address',
        'address',
        'address',
        'uint256',
        'uint256',
        'uint256',
        'uint256',
        'uint256',
        'uint256'
    ]
    order_hash = Web3.soliditySha3(types, values).hex()
    signed_order['order_hash'] = order_hash
    hex_signature = web3.Eth.sign(ETHEREUM_ADDRESS, hexstr=order_hash).hex()
    sig = Web3.toBytes(hexstr=hex_signature)
    v, r, s = Web3.toInt(sig[-1]), Web3.toHex(sig[:32]), Web3.toHex(sig[32:64])
    ec_signature = {'v': v, 'r': r, 's': s}
    signed_order['ec_signature'] = ec_signature

    signed_order['exchange_contract_address'] = signed_order['exchange_contract_address'].lower()
    signed_order['maker'] = signed_order['maker'].lower()
    signed_order['taker'] = signed_order['taker'].lower()
    signed_order['maker_token_address'] = signed_order['maker_token_address'].lower()
    signed_order['taker_token_address'] = signed_order['taker_token_address'].lower()
    signed_order['fee_recipient'] = signed_order['fee_recipient'].lower()

    return signed_order


def authenticated_request(url, method, body):
    timestamp = str(int(round(time.time() * 1000)))
    prehash = API_KEY + timestamp + method + \
        json.dumps(body, separators=(',', ':'))
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'),
                                          msg=prehash.encode('utf-8'),
                                          digestmod=hashlib.sha256).digest())

    headers = {
        'TOX-ACCESS-KEY': API_KEY,
        'TOX-ACCESS-SIGN': signature,
        'TOX-ACCESS-TIMESTAMP': timestamp
    }
    request = requests.request(method,
                               url,
                               headers=headers,
                               json=body)

    return request


def new_market_order(
        base_token_address,
        quote_token_address,
        side,
        order_amount,
        fee_option='fee_option'):
    reserve_body = {
        'base_token_address': base_token_address,
        'quote_token_address': quote_token_address,
        'side': side,
        'order_amount': order_amount,
        'fee_option': fee_option
    }
    reserve_request = authenticated_request(
        RESERVE_MARKET_ORDER, 'POST', reserve_body)
    print(reserve_request.text)
    signed_order = sign_order(json.loads(reserve_request.text)['unsigned_order'])
    market_order_id = json.loads(reserve_request.text)['market_order_id']

    place_body = {
        'market_order_id': market_order_id,
        'signed_order': signed_order
    }

    # place_request = authenticated_request(PLACE_MARKET_ORDER, 'POST', place_body)

    # history_request = authenticated_request(USER_HISTORY, 'GET', {})

# TODO Remove function call
# new_market_order(
#     '0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570',
#     '0xd0a1e359811322d97991e03f863a0c30c2cf029c',
#     'buy',
#     '123456789012345678')
