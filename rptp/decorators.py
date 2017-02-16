import time

import logging
from selenium.common.exceptions import WebDriverException


def wait_page_loaded(func, seconds=2):
    def func_wrapper(*args, **kwargs):
        func(*args, **kwargs)
        time.sleep(seconds)

    return func_wrapper


def handle_driver_closed(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WebDriverException as e:
            logging.info(e)

    return func_wrapper
