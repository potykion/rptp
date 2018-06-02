from itertools import filterfalse
from operator import itemgetter
from typing import List, Dict

from rptp.formatters import format_videos
from rptp import vk_api


async def get_videos(query, token, **kwargs) -> List[Dict]:
    vk_videos = await vk_api.request_videos(query, token, **kwargs)
    adult_videos = filterfalse(itemgetter("can_add"), vk_videos)
    formatted_videos = format_videos(adult_videos)
    return formatted_videos
