import requests

from rptp.config import TOKEN, API_VERSION

API_URL = 'https://api.vk.com/method/'


def execute_api_request(method, **data):
    request_data = data
    request_data.update({
        'access_token': TOKEN,
        'v': API_VERSION
    })

    req = requests.get(API_URL + method, data)
    resp = req.json()['response']
    return resp
