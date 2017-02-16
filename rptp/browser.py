import json
import logging
import os
import re
from collections import namedtuple, defaultdict
from datetime import datetime
from functools import lru_cache
from http.client import CannotSendRequest
from threading import Thread
from typing import List

from selenium import webdriver
import time
from urllib.parse import urlencode, urlparse, parse_qs

from selenium.common.exceptions import WebDriverException, NoSuchElementException

from .config import LOGIN, PASSWORD, SESSION_BASE_PATH
from .decorators import wait_page_loaded, handle_driver_closed

BASE_URL = 'https://vk.com/'
FEED_URL = BASE_URL + 'feed'
VIDEO_URL = BASE_URL + 'video'

DEFAULT_SEARCH_PARAMS = {
    'hd': 1,
    'len': 2,
    'notsafe': 1,
    'order': 0,
}

VideoTimestamp = namedtuple('VideoTimestamp', ['video_id', 'is_playing', 'timestamp'])


@lru_cache(maxsize=None)
def extract_video_id(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    video_id = params.get('z', None)
    if video_id:
        video_id = video_id[0]
        assert re.match('video-?\d+_\d+', video_id)
    return video_id


def group_video_timestamps(video_timestamps: List[VideoTimestamp]):
    grouped = defaultdict(list)

    for vt in video_timestamps:
        if vt.video_id in grouped:
            if grouped[vt.video_id][-1]['is_playing'] == vt.is_playing:
                grouped[vt.video_id][-1]['to'] = vt.timestamp
            else:
                grouped[vt.video_id].append({
                    'from': vt.timestamp,
                    'to': vt.timestamp,
                    'is_playing': vt.is_playing
                })
        else:
            grouped[vt.video_id].append({
                'from': vt.timestamp,
                'to': vt.timestamp,
                'is_playing': vt.is_playing
            })

    return grouped


def update_base(grouped_video_timestamps, path=SESSION_BASE_PATH):
    if os.path.exists(path):
        with open(path) as f:
            base = json.load(f)
    else:
        base = []

    session = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'videos': grouped_video_timestamps
    }

    base.append(session)

    with open(path, 'w') as f:
        json.dump(base, f)


class VideoWatcher(Thread):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def video_is_playing(self):
        try:
            play_button_class = '.videoplayer_controls_item.videoplayer_btn.videoplayer_btn_play'
            button = self.driver.find_element_by_css_selector(play_button_class)
            return button.get_attribute('aria-label') == 'Приостановить'
        except NoSuchElementException:
            return False

    def video_is_opened(self):
        try:
            return VIDEO_URL in self.driver.current_url and extract_video_id(self.driver.current_url) is not None
        except CannotSendRequest:
            return False

    def run(self):
        videos = []

        while True:
            try:
                if self.video_is_opened():
                    videos.append(VideoTimestamp(
                        video_id=extract_video_id(self.driver.current_url),
                        is_playing=self.video_is_playing(),
                        timestamp=datetime.now().timestamp()
                    ))
                time.sleep(1)
            except WebDriverException as e:
                logging.info(e)
                break

        grouped_video_timestamps = group_video_timestamps(videos)

        update_base(grouped_video_timestamps)


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.watcher = VideoWatcher(self.driver)

    def __enter__(self):
        self.login_to_vk()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @handle_driver_closed
    @wait_page_loaded
    def login_to_vk(self, login=LOGIN, password=PASSWORD):
        self.driver.get(BASE_URL)
        self.driver.find_element_by_id("index_email").send_keys(login)
        self.driver.find_element_by_id("index_pass").send_keys(password)
        self.driver.find_element_by_id('index_login_form').submit()

    @handle_driver_closed
    @wait_page_loaded
    def search_videos(self, search_query, **search_params):
        if VIDEO_URL in self.driver.current_url:
            search_field = self.driver.find_element_by_id('video_search_input')
            search_field.clear()
            search_field.send_keys(search_query)
            # search_field.submit()
        else:
            # https://vk.com/video?hd=1&len=2&notsafe=1&order=0&q=Lika
            params = DEFAULT_SEARCH_PARAMS.copy()
            params.update(search_params)
            params['q'] = search_query

            url = '{}?{}'.format(VIDEO_URL, urlencode(params))
            self.driver.get(url)

            if not self.watcher.is_alive():
                self.watcher.start()

    @handle_driver_closed
    def close(self):
        self.driver.close()
