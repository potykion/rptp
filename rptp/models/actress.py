import os
import random
from itertools import chain, groupby
from threading import Thread

from rptp.config import ACTRESS_BASE_PATH, UPDATE_BASE
from rptp.data.urls import ACTRESS_BASE_PAGE
from rptp.models.priority import PriorityModel
from rptp.utils.file_utils import load_json_list, save_as_json
from rptp.utils.web_utils import url_to_soup


class Actress(PriorityModel):
    def __init__(self, name, image, debut_year, url, priority=0):
        super().__init__(priority)
        self.name = name
        self.image = image
        self.debut_year = debut_year
        self.url = url

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(cls, json_):
        actress = cls(**json_)
        return actress

    def __str__(self):
        return self.name


class ActressManager:
    def __init__(self):
        self.actresses = []
        self.used_actresses = []

    def __enter__(self):
        self.load_actresses()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._update_actresses(self.used_actresses)

    def random_pick(self):
        unused_actresses = self.unused_actresses

        if not unused_actresses:
            raise LookupError('No more models to pick!')

        key_func = lambda a: a.priority
        sorted_actresses = sorted(unused_actresses, key=key_func, reverse=True)
        _, actress_grouper = next(groupby(sorted_actresses, key_func))
        actresses = list(actress_grouper)

        actress = random.choice(actresses)
        self.used_actresses.append(actress)

        return actress

    @property
    def unused_actresses(self):
        return [actress for actress in self.actresses if actress not in self.used_actresses]

    def load_actresses(self):
        if os.path.exists(ACTRESS_BASE_PATH):
            json_actresses = load_json_list(ACTRESS_BASE_PATH)

            if UPDATE_BASE:
                self._sync_actress_base(other_thread=True)
        else:
            self._sync_actress_base(other_thread=False)
            json_actresses = load_json_list(ACTRESS_BASE_PATH)

        self.actresses = [Actress.from_json(json_) for json_ in json_actresses]

    def _sync_actress_base(self, other_thread=False):
        if other_thread:
            Thread(target=self._sync_actress_base, daemon=True).start()
        else:
            parsed_actresses = _parse_actress_page(ACTRESS_BASE_PAGE)
            self._extend_actresses(parsed_actresses)

    def _extend_actresses(self, actresses):
        existing_actress_urls = frozenset(actress.url for actress in self.actresses)
        new_actresses = [actress for actress in actresses if actress.url not in existing_actress_urls]

        all_actresses = self.actresses + new_actresses

        self._save_actresses(all_actresses)

    def _update_actresses(self, actresses):
        used_actresses_urls = frozenset(a.url for a in actresses)
        old_actresses = [a for a in self.actresses if a.url not in used_actresses_urls]

        updated_actresses = old_actresses + actresses

        self._save_actresses(updated_actresses)

    def _save_actresses(self, actresses=None, json_file=ACTRESS_BASE_PATH):
        if actresses is None:
            actresses = self.actresses

        actresses = [actress.to_json() for actress in actresses]

        save_as_json(actresses, json_file)


def _parse_actress_page(page_url):
    bs = url_to_soup(page_url)

    actress_blocks = bs.find(id='debut').find_all('tbody')

    return chain.from_iterable(map(_parse_actress_block, actress_blocks))


def _parse_actress_block(actress_block):
    def _actress_from_a_tag(a):
        return Actress(a.text, a['rel'][0], debut_year, a['href'])

    actress_links = actress_block.td.find_all('a')
    debut_year = int(actress_block.th.text)

    yield from map(_actress_from_a_tag, actress_links)
