import requests
from bs4 import BeautifulSoup
from flask import Request


def url_to_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    content = resp.content
    return BeautifulSoup(content, "lxml")


def is_mobile_user_agent(request: Request) -> bool:
    user_agent = str(request.user_agent).lower()
    return any(mobile_user_agent in user_agent for mobile_user_agent in ('iphone', 'android'))
