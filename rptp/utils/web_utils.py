import requests
from bs4 import BeautifulSoup


def url_to_soup(url):
    resp = requests.get(url)
    content = resp.content
    bs = BeautifulSoup(content, "lxml")
    return bs
