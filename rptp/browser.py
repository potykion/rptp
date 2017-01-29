from selenium import webdriver
import time
from urllib.parse import urlencode

from rptp.config import LOGIN, PASSWORD

BASE_URL = 'https://vk.com/'
FEED_URL = BASE_URL + 'feed'
VIDEO_URL = BASE_URL + 'video'

DEFAULT_SEARCH_PARAMS = {
    'hd': 1,
    'len': 2,
    'notsafe': 1,
    'order': 0,
}


def _wait_page_loaded(func):
    def func_wrapper(*args, **kwargs):
        func(*args, **kwargs)
        time.sleep(1)

    return func_wrapper


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.login_to_vk()

    @_wait_page_loaded
    def login_to_vk(self, login=LOGIN, password=PASSWORD):
        self.driver.get(BASE_URL)
        self.driver.find_element_by_id("index_email").send_keys(login)
        self.driver.find_element_by_id("index_pass").send_keys(password)
        self.driver.find_element_by_id('index_login_form').submit()

    @_wait_page_loaded
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

    def close(self):
        self.driver.close()
