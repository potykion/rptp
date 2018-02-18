from urllib.parse import urlencode

import aiohttp


async def request_videos(query, token):
    # https://vk.com/dev/api_requests
    # https://vk.com/dev/video.search
    params = urlencode({
        'q': query,
        'adult': 1,
        'filters': 'mp4,long',
        'hd': 1,
    })
    url = f"https://api.vk.com/method/video.search?{params}&access_token={token}&v=5.73"
    response = await _make_request_async(url)
    return response['response']['items']


async def _make_request_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as result:
            return await result.json()
