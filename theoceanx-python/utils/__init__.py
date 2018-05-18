import time
from .request import Request


def get_ts():
    return round(time.time())


req = Request()

request = req.request
