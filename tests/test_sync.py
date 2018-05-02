from asynctest import patch, CoroutineMock

from rptp.scripts.sync import sync_actresses_without_videos


async def test_sync_actresses_without_videos(loop, sync_db, actress_without_videos, vk_token):
    assert sync_db.actresses.find({'has_videos': False}).count() == len(actress_without_videos)

    with patch('rptp.getters.get_videos',
               CoroutineMock(return_value=[{'url': 'https://vk.com/video150323989_162611387'}])):
        await sync_actresses_without_videos(sync_db, vk_token)

    assert sync_db.actresses.find({'has_videos': False}).count() == 0
