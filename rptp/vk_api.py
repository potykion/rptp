import os
from urllib.parse import urlencode, parse_qs, urlparse

import requests

API_VERSION = 5.64
DEFAULT_OFFSET = 40


def find_videos(query, offset=0, count=DEFAULT_OFFSET, token=None):
    params = {
        'q': query,
        'sort': 0,
        'hd': 1,
        'filters': 'mp4, long',
        'offset': offset,
        'count': count,
        'v': API_VERSION,
        'access_token': token
    }

    if 'IS_HEROKU' in os.environ:
        params.update({
            'adult': 1,
        })
    else:
        params.update({
            'adult': 1,
        })

    base_url = 'https://api.vk.com/method/'
    video_search_url = '{}{}'.format(base_url, 'video.search')

    result = requests.get(video_search_url, params).json()

    if 'response' in result:
        videos = result['response']['items']
        count_ = result['response']['count']
        if params.get('adult'):
            videos = list(filter(lambda video: not video['can_add'], videos))
        return videos, count_

    raise LookupError('Failed to search videos', result['error'])


def generate_auth_link():
    base_url = 'https://oauth.vk.com/authorize'

    auth_params = {
        'client_id': '4865149',
        'redirect_uri': 'https://rptp.herokuapp.com',
        'scope': 'video, offline',
        'v': API_VERSION,
        'response_type': 'code',
        'display': 'mobile'
    }

    auth_url = '{}?{}'.format(base_url, urlencode(auth_params))

    return auth_url


def generate_token_receive_link(code):
    base_url = 'https://oauth.vk.com/access_token'

    token_params = {
        'client_id': '4865149',
        'redirect_uri': 'https://rptp.herokuapp.com',
        'client_secret': os.environ['CLIENT_SECRET'],
        'code': code
    }

    token_url = '{}?{}'.format(base_url, urlencode(token_params))

    return token_url


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


def receive_token_from_validation_url(validation_url):
    resp = requests.get(validation_url)
    result_url = resp.url
    result = parse_qs(urlparse(result_url).fragment)

    if 'access_token' not in result:
        raise LookupError('No token found in validate response url', {
            'validation_url': validation_url,
            'result_url': result_url,
            'result': result
        })

    return result
