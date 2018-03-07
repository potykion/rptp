from rptp.formatters import format_videos
from rptp import vk_api


async def get_videos(query, token):
    vk_videos = await vk_api.request_videos(query, token)
    formatted_videos = format_videos(vk_videos)
    return formatted_videos
