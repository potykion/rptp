import logging
import os
import random

import rptp
from rptp import Browser

logging.getLogger().setLevel(logging.INFO)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    actresses = rptp.load_actresses()
    random.shuffle(actresses)
    actresses = iter(actresses)

    browser = None

    while True:
        command = input('Enter "next" to search videos with another actress:\n')
        if command == "next":
            actress = next(actresses)
            if not browser:
                browser = Browser()
            browser.search_videos(actress['name'])
        else:
            if browser:
                browser.close()
            break
