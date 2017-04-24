from rptp.config import TOKEN
from rptp.vk_api import find_videos


def test_video_search():
    videos = find_videos('sasha', token=TOKEN)
    assert len(videos) == 2
