import pytest

from rptp.video.serializers import VkVideoSerializer


@pytest.fixture()
def vk_video():
    return {
        "id": 456239090,
        "owner_id": -150591454,
        "title": "video 15 [ brazzers tits ass anal sex mofos blowjob moms зрелая мамка секс порно nina elle sasha grey минет сосет]",
        "duration": 1897,
        "description": "video 15 [ brazzers tits ass anal sex mofos blowjob moms зрелая мамка секс порно nina elle sasha grey минет сосет]",
        "date": 1505026871,
        "comments": 0,
        "views": 918,
        "width": 1280,
        "height": 720,
        "photo_130": "https://pp.userapi.com/c840436/v840436648/6590/CNQ84c_KEtI.jpg",
        "photo_320": "https://pp.userapi.com/c840436/v840436648/658e/SN2TXi0lDF0.jpg",
        "photo_800": "https://pp.userapi.com/c840436/v840436648/658d/DYxTGsMuvQc.jpg",
        "first_frame_800": "https://pp.userapi.com/c840235/v840235277/24368/IBxKvpoKe3I.jpg",
        "first_frame_320": "https://pp.userapi.com/c840235/v840235277/24369/Dj77eX9Y94Q.jpg",
        "first_frame_160": "https://pp.userapi.com/c840235/v840235277/2436a/obfdpFykVz8.jpg",
        "first_frame_130": "https://pp.userapi.com/c840235/v840235277/2436b/u1cDJYb8hKY.jpg",
        "player": "https://vk.com/video_ext.php?oid=-150591454&id=456239090&hash=b431cad556f9a0f0&__ref=vk.api&api_hash=15050586756f4e2c20fc7e6c6a8d_GE3DEMZRGMYDS",
        "can_add": 0
    }


def test_vk_video_serializer(vk_video):
    """
    Given video received from VK API,
    When deserialize and validate video,
    Then validation passed,
    And video is formatted.
    """
    serializer = VkVideoSerializer(data=vk_video)

    assert serializer.is_valid()
    assert serializer.validated_data == {
        'title': vk_video['title'],
        'preview': vk_video['photo_320'],
        'url': 'https://m.vk.com/video{}_{}'.format(vk_video['owner_id'], vk_video['id']),
        'duration': vk_video['duration'],
        'views': vk_video['views']
    }
