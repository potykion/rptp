from urllib.parse import urlencode
import requests

from rptp.vk.utils.config import APP_ID, AUTH_REDIRECT_URI, API_VERSION, CLIENT_SECRET


def generate_auth_link():
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
    Get token from auth code.
    :param code: Auth code returned after authorization.
    :return: Token json:
    {"access_token":"533bacf01e11f55b536a565b57531ac114461ae8736d6506a3", "expires_in":43200, '''user_id":66748}
    """
    token_link = generate_token_receive_link(code)
    result = requests.get(token_link).json()
    return result

def generate_token_receive_link(code):
    base_url = 'https://oauth.vk.com/access_token'

    token_params = {
        'client_id': APP_ID,
        'redirect_uri': AUTH_REDIRECT_URI,
        'client_secret': CLIENT_SECRET,
        'code': code
    }

    token_url = '{}?{}'.format(base_url, urlencode(token_params))

    return token_url