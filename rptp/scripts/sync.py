from functools import partial

from rptp.getters import get_videos
from rptp.models import AsyncActressManager


async def check_actress_has_videos(actress, token):
    videos = await get_videos(actress, token)
    return bool(videos)


async def sync_actresses_without_videos(db, token):
    manager = AsyncActressManager(db)
    actresses = await manager.filter_without_videos()

    filter_ = partial(check_actress_has_videos, token=token)
    actresses = filter(filter_, actresses)

    # todo update actresses has_videos (in bulk)


if __name__ == '__main__':
    # todo init db
    # todo get token
    # todo call sync_actresses_without_videos
    pass
