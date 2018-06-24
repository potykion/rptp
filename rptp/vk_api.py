import asyncio
import logging
from urllib.parse import urlencode

import aiohttp

from rptp.config import APP_ID, API_VERSION, AUTH_REDIRECT_URI, CLIENT_SECRET


async def request_videos(query, token, **kwargs):
    # https://vk.com/dev/api_requests
    # https://vk.com/dev/video.search
    params = {
        "q": query,
        "access_token": token,
        "adult": 1,
        "filters": "mp4, long",
        "hd": 1,
        "count": 100,
        "v": API_VERSION,
        **kwargs,
    }
    encoded = urlencode(params)
    url = f"https://api.vk.com/method/video.search?{encoded}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            response = await result.json()
            return response["response"]["items"]


def generate_auth_link():
    params = {
        "scope": "video, offline",
        "response_type": "code",
        "display": "mobile",
        "v": API_VERSION,
        "client_id": APP_ID,
        "redirect_uri": AUTH_REDIRECT_URI,
    }
    encoded = urlencode(params)
    return f"https://oauth.vk.com/authorize?{encoded}"


async def request_token_data(code):
    params = {
        "code": code,
        "client_id": APP_ID,
        "redirect_uri": AUTH_REDIRECT_URI,
        "client_secret": CLIENT_SECRET,
    }
    encoded = urlencode(params)
    url = f"https://oauth.vk.com/access_token?{encoded}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            response_json = await result.json()
            return response_json


async def check_video_is_blocked(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            logging.info(video_url)
            logging.info(response.url)
            logging.info(response.status)

            # 451 = Unavailable For Legal Reasons
            return response.status == 451


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        check_video_is_blocked("https://vk.com/video-123841839_456239509")
    )
    loop.close()

    s = "as"
