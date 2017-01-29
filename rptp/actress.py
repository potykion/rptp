import json
import os
from itertools import chain
from threading import Thread

from .config import ACTRESS_BASE_PATH
from .web import bs_from_url

ACTRESS_BASE_PAGE = 'http://www.pornteengirl.com/debutyear/debut.html'


def load_actresses():
    _update_actress_base(other_thread=os.path.exists(ACTRESS_BASE_PATH))

    with open(ACTRESS_BASE_PATH) as f:
        actresses = json.load(f)

    return actresses


def _update_actress_base(other_thread=False):
    if other_thread:
        Thread(target=_update_actress_base)

    actresses = list(_parse_actress_page(ACTRESS_BASE_PAGE))

    with open(ACTRESS_BASE_PATH, 'w') as f:
        json.dump(actresses, f)


def _parse_actress_page(page_url):
    bs = bs_from_url(page_url)

    actress_blocks = bs.find(id='debut').find_all('tbody')

    return chain.from_iterable(map(_parse_actress_block, actress_blocks))


def _parse_actress_block(actress_block):
    def _actress_from_link(a):
        return {
            'name': a.text,
            'image': a['rel'][0],
            'debut': debut_year
        }

    actress_links = actress_block.td.find_all('a')
    debut_year = int(actress_block.th.text)

    yield from map(_actress_from_link, actress_links)
