from functools import partial


async def check_actress_has_videos(actress, token):
    from rptp.getters import get_videos

    videos = await get_videos(actress, token)
    return bool(videos)


async def sync_actresses_without_videos(db, token):
    from rptp.async_actress import AsyncActressManager

    manager = AsyncActressManager(db)
    actresses = await manager.filter_without_videos()

    filter_ = partial(check_actress_has_videos, token=token)
    actresses = filter(filter_, actresses)

    # todo update actresses has_videos (in bulk)


if __name__ == '__main__':
    s = 'as'
    # todo init db
    # todo get token
    # todo call sync_actresses_without_videos
    pass
