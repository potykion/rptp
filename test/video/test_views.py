from typing import Dict
from unittest import mock
from urllib.parse import urlencode

import pytest
from django.test import Client
from rest_framework.response import Response

from rptp.users.models import User
from test.vk.setup import VkApiTest


@pytest.fixture(autouse=True)
def setup_users(vk_access_token):
    User.objects.create(access_token=vk_access_token, username=16231309)
    User.objects.create(access_token='op', username=1)


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

        response_data = dict(response.data)
        videos = response_data.pop('videos')

        assert response_data == {'offset': 42, 'query': 'Sasha'} and len(videos) == video_count

    def test_video_search_view_for_actress_without_videos(self, client: Client, vk_access_token):
        """
        Given client, and actress without videos,
        When request videos,
        Then response contains no videos.
        """
        with mock.patch('requests.get') as mock_response:
            mock_response.return_value = mock.MagicMock(
                json=lambda: {'response': {'items': []}}
            )

            url = '/api/video/search'
            params = urlencode({
                'query': 'Eszter',
                'offset': 1,
                'access_token': vk_access_token
            })

            response = client.get(f'{url}?{params}')

        assert response.data == {
            'videos': [],
            'offset': 2,
            'query': 'Eszter'
        }

    def test_video_search_view_with_invalid_token(self, client: Client, vk_access_token):
        with mock.patch('requests.get') as mock_resp:
            mock_resp.return_value = mock.MagicMock(
                json=lambda: {'error': 'Error occurred.'}
            )
            url = '/api/video/search'
            params = urlencode({
                'query': 'Eszter',
                'offset': 1,
                'access_token': 'op'
            })

            response = client.get(f'{url}?{params}')

        assert response.status_code == 403
