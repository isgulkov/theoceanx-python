import time
from .request import Request
from .constans import zeroExConfigByNetworkId

def get_ts():
    return round(time.time())


req = Request()

request = req.request
