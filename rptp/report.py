import operator

from dateutil import parser
from jinja2 import Template

from .config import SESSIONS_HTML
from .vk_api import request_video_info


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
        parser.parse(date_).date(): map(format_video, request_video_info(*videos))
        for date_, videos in sessions.items()
    }

    date_sessions = sorted(date_sessions.items(), key=operator.itemgetter(0), reverse=True)
    return date_sessions


def format_video(video):
    return {
        'url': 'https://vk.com/video{owner_id}_{id}'.format(**video),
        'preview': video.get('photo_320'),
        'title': video.get('title')
    }
