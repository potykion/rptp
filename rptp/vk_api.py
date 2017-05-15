import os
from urllib.parse import urlencode, parse_qs, urlparse

import requests
from flask import session
from typing import Dict, Iterable, Any, List, Tuple

# todo as environ vars
# heroku config
APP_ID = 6030754
REDIRECT_URI = 'https://rptp.herokuapp.com/auth'

# vk config
API_BASE_URL = 'https://api.vk.com/method'
API_VERSION = 5.64

# app config
VK_VIDEO_SEARCH_PARAMS = {
    'sort': 0,
    'hd': 1,
    'filters': 'mp4, long',
    'adult': 1,
    'v': API_VERSION
}
VIDEO_COUNT = 3 * 13

VideoList = List[Dict[str, Any]]


def request_adult_videos(query: str, offset: int = 0, count: int = VIDEO_COUNT) -> Tuple[VideoList, int]:
    final_offset = offset
    adult_videos = []

    while len(adult_videos) < count:
        videos = search_videos(query, final_offset, count)
        final_offset += count

        if not videos:
            break

        adult_videos += list(filter_adult_videos(videos))

    return adult_videos[:count], final_offset


def search_videos(query: str, offset: int = 0, count: int = VIDEO_COUNT) -> VideoList:
    token = session.get('access_token')

    video_search_url = f'{API_BASE_URL}/video.search'
    video_search_params = build_video_search_params(query, token, count=count, offset=offset)

    videos_json = requests.get(video_search_url, video_search_params).json()

    return extract_videos(videos_json)


def extract_videos(videos_json: Dict[str, Any]):
    if 'response' not in videos_json:
        raise LookupError('Failed to find videos', videos_json['error'])

    return videos_json['response']['items']


def build_video_search_params(query: str, token: str, **kwargs: Any):
    params = dict(VK_VIDEO_SEARCH_PARAMS)
    params.update({
        'q': query,
        'access_token': token,
    })
    params.update(**kwargs)
    return params


def filter_adult_videos(videos: Iterable[Dict[str, Any]]):
    for video in videos:
        if not video['can_add']:
            yield video


def generate_auth_link():
    base_url = 'https://oauth.vk.com/authorize'

    auth_params = {
        'client_id': APP_ID,
        'redirect_uri': REDIRECT_URI,
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
        'client_id': APP_ID,
        'redirect_uri': REDIRECT_URI,
        # todo rename to VK_CLIENT_SECRET
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
