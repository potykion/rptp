from http.cookies import SimpleCookie
from unittest import mock

import asynctest
import pytest

from rptp.app import app
from rptp.models import AsyncActressManager, ActressPicker


@pytest.fixture
def test_cli(loop, test_client):
    return loop.run_until_complete(test_client(app))


def test_video_api_view(vk_videos):
    """
    Given query and token,
    When create request to videos page,
    Then response contains formatted VK videos.
    """
    query = 'Sasha'
    token = 'ec95bd6b0fa49ed5ea3cdd214b9d49b29ed637bd8c96e4018c0e4b09ebc9de38f10d5484f7af3de0a41ad'

    with mock.patch('rptp.vk_api.request_videos', asynctest.CoroutineMock(return_value=vk_videos)):
        _, response = app.test_client.get(
            '/api/videos',
            params={'query': query},
            headers={'Authorization': token}
        )

        data = response.json

    assert data[0] == {
        'preview': 'https://pp.userapi.com/c627623/v627623889/49c74/1f_JKV_2jBE.jpg',
        'url': 'https://vk.com/video-81447889_456239209',
        'mobile_url': 'https://m.vk.com/video-81447889_456239209',
        'duration': '0:22:52'
    }


def test_auth_template_view_with_code(vk_videos, vk_token_response, vk_token):
    """
    Given code,
    When go to auth template view with code argument,
    Then response redirects to video view,
    And cookies contains token.
    """
    code = '6d69dce5bb3043c054'

    with mock.patch('rptp.vk_api.request_token_data', asynctest.CoroutineMock(return_value=vk_token_response)):
        with mock.patch('rptp.vk_api.request_videos', asynctest.CoroutineMock(return_value=vk_videos)):
            request, response = app.test_client.get(
                '/index', params={'code': code}
            )

    # assert response.url.path_qs == '/videos'
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get('Set-Cookie', {}))
    assert response_cookies['access_token'].value == vk_token


def test_pick_random_api_view(actresses, vk_token):
    """
    Given actresses,
    When make request to pick_random_api_view,
    Then response contains random actress.
    """
    request, response = app.test_client.get(f'/api/pick_random?token={vk_token}')
    assert set(response.json.keys()) == {'name', 'debut_year', 'link'}


async def test_report_api_view(test_cli, actresses, vk_token, actress_picker: ActressPicker):
    """
    Given actress name,
    When make request to report_api_view,
    Then actress has_videos flag set to False.
    """
    actress_name = 'Cynthia Thomas'


    response = await test_cli.get(f'/api/report?query={actress_name}&token={vk_token}')
    actress = await actress_picker.pick_by_name(actress_name)
    assert actress['has_videos'] is False
