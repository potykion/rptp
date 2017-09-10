from unittest import mock

from test.vk.setup import VkApiTest


class TestUtils(VkApiTest):
    def test_vk_api(self, vk_api):
        """
        Given vk api instance,
        When get several attributes from vk api,
        And convert vk api to string,
        Then result string contains attributes separated by dot.
        """
        assert str(vk_api.video.search) == 'video.search'

    def test_vk_api_call(self, vk_api, vk_video_search_results):
        """
        Given vk api instance,
        When call vk api with several args,
        Then call result equals to real vk api response.
        """
        with mock.patch('requests.get') as mock_response:
            mock_response.return_value = mock.MagicMock(
                json=lambda: vk_video_search_results
            )

            response = vk_api.video.search(q='Sasha', count=200)

        assert response == vk_video_search_results
