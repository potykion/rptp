from .video import start_watch_videos
from .report import start_generate_report


def change_mode(mode):
    if mode == 'video':
        start_watch_videos()
    elif mode == 'report':
        start_generate_report()
