from rptp.formatters import format_videos
from rptp.vk_api import request_videos


async def video_getter(query, token):
    vk_videos = await request_videos(query, token)
    formatted_videos = format_videos(vk_videos)
    return formatted_videos
