

"""
E-commerce platform Shoper REST API Wrapper
"""

__version__ = '1.0.0'
__author__ = 'P'
__license__ = 'MIT'

from .base import ShoperBaseApi
from .shoperapi import ShoperWrapper


class ShoperClient(ShoperBaseApi):
    """
    Shoper REST API Client - handles all endpoints with magic.
    Converts attribute to resource endpoint

    :param api_url: (required) Shoper REST API url (ex. 'https://shop11111.shoparena.pl/webapi/rest')
    :type api_url: str
    :param client_login: (optional) Shoper consumer key
    :type client_login: str
    :param client_secret: (optional) Shoper consumer secret
    :type client_secret: str
    :param access_token: (optional) Shoper consumer access_token
    :type access_token: str
    :param refresh_token: (optional) Shoper consumer refresh_token
    :type refresh_token: str
    """

    def __init__(self, api_url, client_login=None, client_secret=None, access_token=None, refresh_token=None):
        super(ShoperClient, self).__init__(api_url, client_login, client_secret, access_token, refresh_token)

    def __getattr__(self, name):
        return ShoperWrapper(self, str(name).replace('_', '-'))
