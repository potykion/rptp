import asyncio
from urllib.parse import urlencode

import aiohttp

from rptp.config import APP_ID, API_VERSION, AUTH_REDIRECT_URI, CLIENT_SECRET


async def request_videos(query, token):
    # https://vk.com/dev/api_requests
    # https://vk.com/dev/video.search
    params = {
        'q': query,
        'access_token': token,

        'adult': 1,
        'filters': 'mp4, long',
        'hd': 1,

        'v': API_VERSION
    }
    encoded = urlencode(params)
    url = f"https://api.vk.com/method/video.search?{encoded}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            response = await result.json()
            return response['response']['items']


def generate_auth_link():
    params = {
        'scope': 'video, offline',
        'response_type': 'code',
        'display': 'mobile',

        'v': API_VERSION,
        'client_id': APP_ID,
        'redirect_uri': AUTH_REDIRECT_URI,
    }
    encoded = urlencode(params)
    return f'https://oauth.vk.com/authorize?{encoded}'


async def request_token_data(code):
    params = {
        'code': code,

        'client_id': APP_ID,
        'redirect_uri': AUTH_REDIRECT_URI,
        'client_secret': CLIENT_SECRET,
    }
    encoded = urlencode(params)
    url = f'https://oauth.vk.com/access_token?{encoded}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            response = await result.json()
            return response
