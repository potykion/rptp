from itertools import islice
from typing import Tuple, Iterable, Dict

from rptp.common.utils import last


def filter_adult_videos(vk_videos: Iterable[Dict], required_count=30) -> Tuple[Iterable, int]:
    """
    Filter adult vk videos.

    Args:
        vk_videos: List of VK-videos.
        required_count: Required adult videos count.

    Returns:
        List of adult videos and index of last video in input list.

    >>> videos, index = filter_adult_videos([
    ...     {'can_add': False},
    ...     {'can_add': True},
    ...     {'can_add': False},
    ...     {'can_add': False}
    ... ], 2)
    >>> videos = list(videos)
    >>> len(videos)
    2
    >>> index
    2
    """
    adult_videos = (
        (index, video)
        for index, video in enumerate(vk_videos)
        if not video['can_add']
    )

    index, videos = zip(*islice(adult_videos, required_count))

    return videos, last(index)
