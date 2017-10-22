from typing import Dict
from unittest import mock
from urllib.parse import urlencode

import pytest
from django.test import Client
from rest_framework.response import Response

from rptp.users.models import User
from test.vk.setup import VkApiTest


@pytest.fixture(autouse=True)
def setup_user(vk_access_token):
    User.objects.create(access_token=vk_access_token)


@pytest.mark.django_db
class TestViews(VkApiTest):
    def test_adult_videos_search_view(self, client: Client, vk_access_token: str, vk_video_search_results: Dict):
        """
        Given client, access token, video count,
        When request videos,
        Then response contains offset and videos
        """
        video_count = 30

        with mock.patch('requests.get') as mock_response:
            mock_response.return_value = mock.MagicMock(
                json=lambda: vk_video_search_results
            )

            url = '/api/video/search'
            params = urlencode({
                'query': 'Sasha',
                'count': video_count,
                'access_token': vk_access_token
            })

            response = client.get(f'{url}?{params}')

        assert 'offset' in response.data and len(response.data['videos']) == video_count
