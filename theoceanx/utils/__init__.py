import time
from .request import Request
from .constants import zeroExConfigByNetworkId

def get_ts():
    return round(time.time())


req = Request()

request = req.request
