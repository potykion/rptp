from urllib.parse import urlencode
import requests

from rptp.vk.utils.config import APP_ID, AUTH_REDIRECT_URI, API_VERSION, CLIENT_SECRET


def generate_auth_link():
    """
    Generate authorization url.
    Returns:
        Authorization url.

    """
    base_url = 'https://oauth.vk.com/authorize'

    auth_params = {
        'client_id': APP_ID,
        'redirect_uri': AUTH_REDIRECT_URI,
        'scope': 'video, offline',
        'v': API_VERSION,
        'response_type': 'code',
        'display': 'mobile'
    }

    auth_url = '{}?{}'.format(base_url, urlencode(auth_params))

    return auth_url


def receive_token_from_code(code):
    """
    Request token data by input code.

    Args:
        code: Code for token receive.

    Returns:
        Token request data.
    """
    base_url = 'https://oauth.vk.com/access_token'

    token_params = {
        'client_id': APP_ID,
        'redirect_uri': AUTH_REDIRECT_URI,
        'client_secret': CLIENT_SECRET,
        'code': code
    }

    token_url = '{}?{}'.format(base_url, urlencode(token_params))

    return requests.get(token_url).json()
