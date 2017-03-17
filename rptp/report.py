import operator
import time

from dateutil import parser
from jinja2 import Template

from rptp.vk_api import find_videos

SESSIONS_HTML = 'sessions.html'


def form_sessions_report(sessions):
    with open('templates/sessions.html') as f:
        template = Template(f.read())

    date_sessions = format_sessions(sessions)

    context = {
        'sessions': date_sessions
    }
    html = template.render(**context)

    with open(SESSIONS_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    return html


def format_sessions(sessions):
    date_sessions = {
        parser.parse(date_).date(): request_video_info(videos)
        for date_, videos in sessions.items()
    }

    date_sessions = sorted(date_sessions.items(), key=operator.itemgetter(0), reverse=True)
    return date_sessions


def request_video_info(video_urls):
    videos = find_videos([video.strip('video') for video in video_urls])

    video_info = []

    for video_url in video_urls:
        video_dict = next(
            (video for video in videos if 'video{owner_id}_{id}'.format(**video) == video_url), None
        )

        if video_dict:
            video_info.append({
                'url': 'https://vk.com/{}'.format(video_url),
                'preview': video_dict.get('photo_320'),
                'title': video_dict.get('title')
            })

    return video_info
