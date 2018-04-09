from rptp.models import AsyncActressManager
from tests.fixtures import ActressFixtures


class TestModels(ActressFixtures):
    async def test_upload_actresses(self, actresses, async_actress_manager: AsyncActressManager):
        """
        Given parsed actresses,
        When insert them to actress collection,
        Then actress collection contains parsed actresses,
        And Miss Blackberry too.
        """

        assert len(actresses) == await async_actress_manager.count()

        miss_blackberry = 'Miss Blackberry'
        miss_blackberry = await async_actress_manager.find(miss_blackberry)
        miss_blackberry.pop('_id', None)
        assert miss_blackberry == {
            'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
            'debut_year': 2015,
            'name': 'Miss Blackberry'
        }

    async def test_mark_no_videos(self, actresses, async_actress_manager: AsyncActressManager):
        """
        Given actresses,
        When report actress,
        Then actress has_videos flag is false.
        """
        actress = await async_actress_manager.find('Wilda')

        actress_name = actress['name']
        async_actress_manager.mark_no_videos(actress_name)

        actress = await async_actress_manager.find(actress_name)
        assert not actress['has_videos']
