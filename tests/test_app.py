import json
import os
from http.cookies import SimpleCookie
from unittest import mock

import pytest

from rptp.app import app
from rptp.config import BASE_DIR


@pytest.fixture()
async def vk_video_response():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)


@pytest.fixture()
async def vk_videos():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)['response']['items']

@pytest.fixture()
async def vk_token_response():
    return {
        "access_token": "32fb57fa0c146de382e9433a48c032e73ca159450460d463987ce9b52943846540c6899af777a49977346",
        "expires_in": 0,
        "user_id": 16231309
    }


@pytest.fixture()
def vk_token():
    return '32fb57fa0c146de382e9433a48c032e73ca159450460d463987ce9b52943846540c6899af777a49977346'


@pytest.fixture()
def vk_user():
    return 16231309


def test_video_api_view(vk_videos):
    """
    Given query and token,
    When create request to videos page,
    Then response contains formatted VK videos.
    """
    query = 'Sasha'
    token = 'ec95bd6b0fa49ed5ea3cdd214b9d49b29ed637bd8c96e4018c0e4b09ebc9de38f10d5484f7af3de0a41ad'

    with mock.patch('rptp.vk_api.request_videos', return_value=vk_videos):
        request, response = app.test_client.get(
            '/api/videos',
            params={'query': query},
            headers={'Authorization': token}
        )

    assert response.json[0] == {
        'preview': 'https://pp.userapi.com/c627623/v627623889/49c74/1f_JKV_2jBE.jpg',
        'url': 'https://vk.com/video-81447889_456239209',
        'mobile_url': 'https://m.vk.com/video-81447889_456239209',
        'duration': '0:22:52'
    }


def test_auth_template_view_with_code(vk_token_response, vk_token, vk_videos):
    """
    Given code,
    When go to auth template view with code argument,
    Then response redirects to video view,
    And cookies contains token.
    """
    code = '6d69dce5bb3043c054'

    with mock.patch('rptp.vk_api.request_token_data', return_value=vk_token_response):
        with mock.patch('rptp.vk_api.request_videos', return_value=vk_videos):

            request, response = app.test_client.get(
                '/index', params={'code': code}
            )

    # assert response.url.path_qs == '/videos'
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get('Set-Cookie', {}))
    assert response_cookies['access_token'].value == vk_token
