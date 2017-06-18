import requests
from bs4 import BeautifulSoup
from flask import Request


def url_to_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    content = resp.content
    return BeautifulSoup(content, "lxml")