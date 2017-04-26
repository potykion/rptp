import os
import time
from functools import wraps
from urllib.parse import urlencode

import requests
import vk

# from rptp.config import TOKEN, SCOPE, APP_ID, PASSWORD, LOGIN, API_VERSION
from bs4 import BeautifulSoup
from flask import session

from rptp.utils.web_utils import url_to_soup

API_VERSION = 5.63

api = None


def create_api():
    global api

    if 'IS_HEROKU' in os.environ:
        TOKEN = os.environ['TOKEN']
    else:
        from .config import TOKEN

    session = vk.Session(TOKEN)
    api = vk.API(session)


# def request_token():
#     session = vk.AuthSession(
#         user_login=LOGIN,
#         user_password=PASSWORD,
#         app_id=APP_ID,
#         scope=SCOPE,
#     )
#     return session.access_token


def init_api(func):
    @wraps(func)
    def init_api_wrapper(*args, **kwargs):
        if not api:
            create_api()
        return func(*args, **kwargs)

    return init_api_wrapper


@init_api
def request_video_info(*video_urls):
    video_ids = [video_url.strip('video') for video_url in video_urls]

    videos = api.video.get(videos=','.join(video_ids), v=API_VERSION, extended=1)['items']
    time.sleep(0.5)
    return videos


def find_videos(query, offset=0, count=20, token=None):
    params = {
        'q': query,
        'sort': 0,
        'hd': 1,
        'filters': 'mp4, long',
        'offset': offset,
        'count': count,
        'v': 5.63,
        'access_token': token
    }

    if 'IS_HEROKU' in os.environ:
        params.update({
            'adult': 1,
        })

    base_url = 'https://api.vk.com/method/'
    video_search_url = '{}{}'.format(base_url, 'video.search')

    result = requests.get(video_search_url, params).json()

    if 'response' in result:
        return result['response']

    raise LookupError('Failed to search videos: {}'.format(result['error']))


def generate_auth_link():
    base_url = 'https://oauth.vk.com/authorize'

    auth_params = {
        'client_id': '4865149',
        'redirect_uri': 'https://rptp.herokuapp.com',
        'scope': 'video',
        'v': 5.63,
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
