import json
import os
from unittest import mock

import pytest

from rptp.app import app
from rptp.config import BASE_DIR


@pytest.fixture()
async def vk_video_response():
    path = os.path.join(BASE_DIR, 'static', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)


def test_video_api_view(vk_video_response):
    """
    Given query and token,
    When create request to videos page,
    Then response contains formatted VK videos.
    """
    query = 'Sasha'
    token = 'ec95bd6b0fa49ed5ea3cdd214b9d49b29ed637bd8c96e4018c0e4b09ebc9de38f10d5484f7af3de0a41ad'

    with mock.patch('rptp.vk_api._make_request_async', return_value=vk_video_response):
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
