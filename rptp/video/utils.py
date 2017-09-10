from itertools import islice
from typing import Tuple, Iterable


def last(iterator, default=None):
    """
    Returns last element of iterable.

    >>> last(iter([1, 2, 3]))
    3
    """

    result = default

    for result in iterator:
        pass

    return result


def filter_adult_videos(vk_videos, required_count) -> Tuple[Iterable, int]:
    """
    Returns adult videos and index of last video related to input videos.

    >>> videos, index = filter_adult_videos([{'can_add': False}, {'can_add': True}, {'can_add': False}, {'can_add': False}], 2)
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


def format_vk_videos(vk_videos) -> Iterable:
    """
    Returns iterator of formatted vk videos.

    >>> videos = [{
    ...     "id": 456239090,
    ...     "owner_id": -150591454,
    ...     "title": "video 15 [ brazzers tits ass anal sex mofos blowjob moms зрелая мамка секс порно nina elle sasha grey минет сосет]",
    ...     "duration": 1897,
    ...     "description": "video 15 [ brazzers tits ass anal sex mofos blowjob moms зрелая мамка секс порно nina elle sasha grey минет сосет]",
    ...     "date": 1505026871,
    ...     "comments": 0,
    ...     "views": 918,
    ...     "width": 1280,
    ...     "height": 720,
    ...     "photo_130": "https://pp.userapi.com/c840436/v840436648/6590/CNQ84c_KEtI.jpg",
    ...     "photo_320": "https://pp.userapi.com/c840436/v840436648/658e/SN2TXi0lDF0.jpg",
    ...     "photo_800": "https://pp.userapi.com/c840436/v840436648/658d/DYxTGsMuvQc.jpg",
    ...     "first_frame_800": "https://pp.userapi.com/c840235/v840235277/24368/IBxKvpoKe3I.jpg",
    ...     "first_frame_320": "https://pp.userapi.com/c840235/v840235277/24369/Dj77eX9Y94Q.jpg",
    ...     "first_frame_160": "https://pp.userapi.com/c840235/v840235277/2436a/obfdpFykVz8.jpg",
    ...     "first_frame_130": "https://pp.userapi.com/c840235/v840235277/2436b/u1cDJYb8hKY.jpg",
    ...     "player": "https://vk.com/video_ext.php?oid=-150591454&id=456239090&hash=b431cad556f9a0f0&__ref=vk.api&api_hash=15050586756f4e2c20fc7e6c6a8d_GE3DEMZRGMYDS",
    ...     "can_add": 0
    ... }]
    >>> formatted_video = list(format_vk_videos(videos))[0]
    >>> all([
    ...     (formatted_video .keys()) == {'title', 'preview', 'url', 'duration', 'views'},
    ...     formatted_video['url'] == 'https://m.vk.com/video-150591454_456239090',
    ...     formatted_video['preview'] == videos[0]['photo_320'],
    ... ])
    True
    """
    return map(
        lambda video: {
            'title': video['title'],
            'preview': video['photo_320'],
            'url': f"https://m.vk.com/video{video['owner_id']}_{video['id']}",
            'duration': video['duration'],
            'views': video['views']
        },
        vk_videos
    )
