import time
from functools import wraps

import vk

from rptp.config import TOKEN, SCOPE, APP_ID, PASSWORD, LOGIN, API_VERSION

api = None


def create_api():
    global api
    session = vk.Session(TOKEN)
    api = vk.API(session)


def request_token():
    session = vk.AuthSession(
        user_login=LOGIN,
        user_password=PASSWORD,
        app_id=APP_ID,
        scope=SCOPE,
    )
    return session.access_token


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


@init_api
def find_videos(query, offset=0, count=20):
    params = {
        'q': query,
        'sort': 0,
        'hd': 1,
        # 'adult': 1,
        'filters': 'mp4, long',
        'offset': offset,
        'count': count,
        'v': 5.63
    }

    videos = api.video.search(**params)
    return videos
