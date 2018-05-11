
from socketIO_client_nexus import SocketIO
import pprint

pp = pprint.PrettyPrinter(indent=4)


def on_message(*args):
    print('message')
    pp.pprint(args)


def on_connect():
    print('connect')


with SocketIO('https://dev-ws.theoceanx.com', 443) as socketIO:
    socketIO.emit('data', {
        'type': 'subscribe',
        'channel': 'order_book',
        'payload': {
            'baseTokenAddress': '0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570',
            'quoteTokenAddress': '0xd0a1e359811322d97991e03f863a0c30c2cf029c',
            'snapshot': 'true',
            'depth': '100'
        }
    })

    socketIO.on('message', on_message)
    socketIO.on('connect', on_connect)
    socketIO.wait(seconds=5)
