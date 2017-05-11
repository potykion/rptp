import pytest

from rptp.config import TOKEN
from rptp.vk_api import find_videos


@pytest.mark.parametrize('q, count', [
    ('sasha', 40),
    ('Grace C', 40),
    ('Melanie Rios', 40)
])
def test_video_search(q, count):
    videos, _ = find_videos(q, count=count, token=TOKEN)
    assert len(videos) == count
