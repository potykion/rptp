import asyncio
import operator
from itertools import filterfalse
from operator import itemgetter
from typing import List, Dict

from rptp.formatters import format_videos
from rptp import vk_api
from rptp.vk_api import check_video_is_blocked


async def get_videos(query, token, **kwargs) -> List[Dict]:
    vk_videos = await vk_api.request_videos(query, token, **kwargs)

    adult_videos = filterfalse(itemgetter("can_add"), vk_videos)
    videos = format_videos(adult_videos)

    return videos
