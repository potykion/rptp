import requests
from bs4 import BeautifulSoup


def bs_from_url(url):
    resp = requests.get(url)
    content = resp.content
    bs = BeautifulSoup(content, "lxml")
    return bs
