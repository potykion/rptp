import time
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


def find_videos(video_ids):
    if not api:
        create_api()

    videos = api.video.get(videos=','.join(video_ids), v=API_VERSION)['items']
    time.sleep(0.5)
    return videos
