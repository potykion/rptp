import time
from threading import Thread
from urllib.parse import urlencode, quote

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from rptp.config import LOGIN, PASSWORD, DEFAULT_SEARCH_PARAMS
from rptp.decorators import retry_if_http_error
from rptp.desktop.data.urls import VK_VIDEO_URL, VK_BASE_URL
from rptp.watcher import VideoWatcher


class Browser(Thread):
    def __init__(self):
        super().__init__()
        self.driver = None
        self._query = ''
        self.new_query = ''
        self.watcher = VideoWatcher(self)

    def __enter__(self):
        self.start()
        return self

    def run(self):
        if not self.driver:
            self.driver = webdriver.Chrome()

        while True:
            try:
                if self.check_user_authorized():
                    if not self.watcher.is_alive():
                        self.watcher.start()
                    self.check_for_videos()
                else:
                    self.login_to_vk()
            except WebDriverException:
                break
            time.sleep(2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def login_to_vk(self, login=LOGIN, password=PASSWORD):
        self.driver.get(VK_BASE_URL)
        self.driver.find_element_by_id("index_email").send_keys(login)
        self.driver.find_element_by_id("index_pass").send_keys(password)
        self.driver.find_element_by_id('index_login_form').submit()
        time.sleep(2)

    @retry_if_http_error
    def search_videos(self, search_query):
        self._query = search_query

        try:
            if VK_VIDEO_URL in self.driver.current_url:
                search_field = self.driver.find_element_by_id('video_search_input')
                search_field.clear()
                search_field.send_keys(search_query)
            else:
                # https://vk.com/video?hd=1&len=2&notsafe=1&order=0&q=Lika
                params = DEFAULT_SEARCH_PARAMS.copy()
                params['q'] = search_query

                url = '{}?{}'.format(VK_VIDEO_URL, urlencode(params))
                self.driver.get(url)

            return True
        except WebDriverException:
            return False

    def close(self):
        try:
            self.driver.close()
        except WebDriverException:
            pass

    @retry_if_http_error
    def get_info(self):
        try:
            return self._query, self.driver.current_url
        except WebDriverException:
            return ()

    @retry_if_http_error
    def check_user_authorized(self):
        if VK_BASE_URL not in self.driver.current_url:
            self.driver.get(VK_BASE_URL)
        try:
            self.driver.find_element_by_id('top_profile_link')
            return True
        except WebDriverException:
            return False

    @retry_if_http_error
    def check_for_videos(self):
        if self.new_query and quote(self.new_query) not in self.driver.current_url:
            self.search_videos(self.new_query)
            if self.new_query != self._query:
                self._query = self.new_query

    def request_videos(self, query):
        self.new_query = query
