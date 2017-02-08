import json
import os
import random
from itertools import chain
from threading import Thread

from .config import ACTRESS_BASE_PATH
from .web import bs_from_url

ACTRESS_BASE_PAGE = 'http://www.pornteengirl.com/debutyear/debut.html'


class NoMoreActressException(Exception):
    pass


class ActressManager:
    def __init__(self):
        self.actresses = []
        self.used_actresses = []
        self.low_priority_actresses = []

    def __enter__(self):
        self.load_actresses()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._update_actresses(self.used_actresses)

    def random_actress(self):
        while True:
            if len(self.used_actresses) == len(self.actresses):
                raise NoMoreActressException('No more models to pick including low-priority ones.')

            actress = random.choice(self.actresses)

            priority_checked = actress not in self.low_priority_actresses or \
                               actress in self.low_priority_actresses and self.low_priority_actress_can_be_picked

            if priority_checked and actress not in self.used_actresses:
                self.used_actresses.append(actress)
                return actress

    def load_actresses(self):
        if os.path.exists(ACTRESS_BASE_PATH):
            with open(ACTRESS_BASE_PATH) as f:
                self.actresses = json.load(f)
            self._sync_actress_base(other_thread=True)
        else:
            self._sync_actress_base(other_thread=False)
            with open(ACTRESS_BASE_PATH) as f:
                self.actresses = json.load(f)

        self.low_priority_actresses = [a for a in self.actresses if a['priority'] < 0]

    def _sync_actress_base(self, other_thread=False):
        if other_thread:
            Thread(target=self._sync_actress_base).start()
        else:
            parsed_actresses = list(_parse_actress_page(ACTRESS_BASE_PAGE))
            self._extend_actresses(parsed_actresses)

    def _extend_actresses(self, actresses):
        existing_actress_urls = frozenset(a['url'] for a in self.actresses)
        new_actresses = [a for a in actresses if a['url'] not in existing_actress_urls]

        all_actresses = self.actresses + new_actresses

        self._save_actresses(all_actresses)

    def _update_actresses(self, actresses):
        used_actresses_urls = frozenset(a['url'] for a in actresses)
        old_actresses = [a for a in self.actresses if a['url'] not in used_actresses_urls]

        updated_actresses = old_actresses + actresses

        self._save_actresses(updated_actresses)

    def _save_actresses(self, actresses=None):
        if actresses is None:
            actresses = self.actresses

        with open(ACTRESS_BASE_PATH, 'w') as f:
            json.dump(actresses, f)

    @property
    def low_priority_actress_can_be_picked(self):
        return len(self.used_actresses) == len(self.actresses) - len(self.low_priority_actresses)


def _parse_actress_page(page_url):
    bs = bs_from_url(page_url)

    actress_blocks = bs.find(id='debut').find_all('tbody')

    return chain.from_iterable(map(_parse_actress_block, actress_blocks))


def _parse_actress_block(actress_block):
    def _actress_from_link(a):
        return {
            'name': a.text,
            'image': a['rel'][0],
            'debut': debut_year,
            'url': a['href'],
            'priority': 0
        }

    actress_links = actress_block.td.find_all('a')
    debut_year = int(actress_block.th.text)

    yield from map(_actress_from_link, actress_links)
