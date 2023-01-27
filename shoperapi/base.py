import time
import requests
import logging
from requests.auth import HTTPBasicAuth, AuthBase

from .error import ShoperError

_logger = logging.getLogger(__name__)


class HTTPBearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return r


class ShoperBaseApi(object):
    USER_AGENT = 'python-shoperapi'

    def __init__(self, api_url, client_id=None, client_secret=None, access_token=None, refresh_token=None):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

        self._max_retries = 10

    def get_user_token(self, client_id=None, client_secret=None):
        _logger.info(u'Getting token...')

        if client_id:
            self.client_id = client_id

        if client_secret:
            self.client_secret = client_secret

        auth_url = '{}/auth'.format(self.api_url)
        try:
            response = requests.post(auth_url, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        except requests.exceptions.RequestException as e:
            raise e

        if response.status_code >= 400:
            _logger.error(u'FAILED to get token')

            raise ShoperError(response.json())

        _response_json = response.json()

        self.access_token = _response_json.get('access_token')
        self.refresh_token = _response_json.get('refresh_token')

        _logger.info(u'GOT token!')

        return _response_json

    def _get_url(self, endpoint):
        """
        Get URL for requests

        :param endpoint: Shoper Rest API endpoint
        :type endpoint: str
        """

        if endpoint.endswith("/") is False:
            return '{}/{}'.format(self.api_url, endpoint)

    @property
    def _default_headers(self):
        headers = dict()
        headers['User-Agent'] = self.USER_AGENT
        headers['Content-Type'] = 'application/json'

        return headers

    def _request(self, method, endpoint, **kwargs):
        """
        Do requests

        :param method: HTTP method (PUT, POST, GET, DELETE)
        :type method: str
        :param endpoint: Shoper Rest API endpoint
        :type endpoint: str
        :kwargs: args for requests (params, data, etc.)
        """

        headers = self._default_headers
        url = self._get_url(endpoint)

        _logger.info(u'{} Request: {}'.format(method, url))

        if kwargs.get('json'):
            _logger.info(u'PAYLOAD: {json}'.format(**kwargs))

        if kwargs.get('params'):
            _logger.info(u'PARAMS: {params}'.format(**kwargs))

        # Register how many times tried to resend same request
        _tries = kwargs.pop('tries', 0) + 1

        if _tries > self._max_retries:
            _logger.error(u'Maximum retries reached!')
            raise ShoperError("Maximum retries reached!")

        try:
            response = requests.request(method, url, headers=headers, auth=HTTPBearerAuth(self.access_token), **kwargs)
        except requests.exceptions.RequestException as e:
            raise e

        if response.status_code == 429:
            _logger.info(u'HTTP 429: Too much requests')

            # Too many requests - leaky bucket exhausted
            _requests_bandwidth = response.headers['X-SHOP-API-BANDWIDTH']
            _requests_limit = response.headers['X-SHOP-API-LIMIT']

            # Calculate how many seconds to wait
            _timeout = int(_requests_limit) / int(_requests_bandwidth)

            time.sleep(_timeout)

            # Try again
            return self._request(method, endpoint, tries=_tries, **kwargs)
        elif response.status_code == 401:
            _logger.info(u'HTTP 401: Try getting new token')
            # Try to refresh token
            self.get_user_token()

            # Try again
            return self._request(method, endpoint, tries=_tries, **kwargs)
        elif response.status_code >= 400:
            raise ShoperError(response.json())
        else:
            return response.json()

    def _get(self, endpoint, params=None):
        """ Get requests """
        return self._request("GET", endpoint, params=params)

    def _post(self, endpoint, params=None, data=None):
        """ POST requests """
        return self._request("POST", endpoint, params=params, json=data)

    def _put(self, endpoint, params=None, data=None):
        """ PUT requests """
        return self._request("PUT", endpoint, params=params, json=data)

    def _delete(self, endpoint, params=None):
        """ DELETE requests """
        return self._request("DELETE", endpoint, params=params)
