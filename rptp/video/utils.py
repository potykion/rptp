from itertools import islice
from typing import Tuple, Iterable, Dict, List

from rptp.common.utils import last


def filter_adult_videos(vk_videos: Iterable[Dict], required_count=30, initial_offset=0) -> Tuple[List, int]:
    """
    Filter adult vk videos.

    Args:
        vk_videos: List of VK-videos.
        required_count: Required adult videos count.
        initial_offset: Initial offset.

    Returns:
        List of adult videos and index of last video in input list.

    >>> videos, index = filter_adult_videos([
    ...     {'can_add': False},
    ...     {'can_add': True},
    ...     {'can_add': False},
    ...     {'can_add': False}
    ... ], 2)
    >>> len(videos)
    2
    >>> index
    3
    >>> videos, index = filter_adult_videos([], 2)
    >>> videos == [] and index == 1
    True
    """
    adult_videos = (
        (index, video)
        for index, video in enumerate(vk_videos)
        if not video['can_add']
    )

    try:
        index, videos = zip(*islice(adult_videos, required_count))
        return list(videos), last(index) + initial_offset + 1
    except ValueError:
        return [], initial_offset + 1
