import re
import time
from datetime import datetime
from functools import lru_cache
from threading import Thread
from urllib.parse import urlparse, parse_qs

from collections import defaultdict

from .browser import VIDEO_URL
from .config import SESSION_BASE_PATH
from .utils import update_json_list


@lru_cache(maxsize=None)
def extract_video_id(url):
    video_id = None

    if VIDEO_URL in url:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        video_id = params.get('z', None)
        if video_id:
            video_id = video_id[0]
            assert re.match('video-?\d+_\d+', video_id)

    return video_id


class VideoWatcher(Thread):
    def __init__(self, browser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser = browser

    def run(self):
        start_timestamp = datetime.now().timestamp()
        queries = self._watch_for_videos()

        if queries:
            session = (start_timestamp, {query: list(videos) for query, videos in queries.items()})
            update_json_list([session], SESSION_BASE_PATH)

    def _watch_for_videos(self):
        queries = defaultdict(set)

        while True:
            info = self.browser.get_info()
            if info:
                query, url = info
                video_id = extract_video_id(url)

                if video_id:
                    queries[query].add(video_id)

                time.sleep(1)
            else:
                break

        return queries
