import base64
import hashlib
import hmac

import aiohttp

from ..config import get_config
from ..utils import get_ts, request


class Auth:
    # Credentials for API key user
    _api_key = None
    _secret = None

    # Credentials for dashboard user
    _username = None  # currently this is email
    _access_token = None
    _id_token = None
    _refresh_token = None

    async def set_dashboard_user_tokens(self, username, access_token, id_token, refresh_token):
        self._username = username
        self._access_token = access_token
        self._id_token = id_token
        self._refresh_token = refresh_token

    async def set_api_key(self, api_key, secret):
        self._api_key = api_key
        self._secret = secret

    async def refresh_tokens(self):
        if not self._username or not self._refresh_token:
            return

        response = await request({
            'method': 'POST',
            'url': '',  # urljoin(getConfig().api.baseURL, getConfig().api.AUTH_REFRESH),
            'body': {
                'user_id': self._username,
                'refresh_token': self._refresh_token.token
            }
        })

        if response.body.accessToken:
            self._access_token = response.body.accessToken
            self._id_token = response.body.idToken
            self._refresh_token = response.body.refreshToken

    def get_api_key_signature(self, timestamp, method, body):

        # Create the pre_hash string by concatenating required parts
        pre_hash = '{}{}{}{}'.format(self._api_key, timestamp, method, body)

        # Create a sha256 hmac with the secret
        hm = base64.b64encode(hmac.new(self._secret, pre_hash, digestmod=hashlib.sha256).digest())

        return hm

    # TODO setAuthHeaders
    # TODO getWsAuthQuery
    # TODO isDashboardAuth
    # TODO authRequestWrapper
