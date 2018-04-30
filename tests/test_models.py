from rptp.models import AsyncActressManager, ActressPicker


async def test_upload_actresses(loop, actresses, async_actress_manager: AsyncActressManager, actress_picker: ActressPicker):
    """
    Given parsed actresses,
    When insert them to actress collection,
    Then actress collection contains parsed actresses,
    And Miss Blackberry too.
    """

    assert len(actresses) == await async_actress_manager.count()

    miss_blackberry = 'Miss Blackberry'
    miss_blackberry = await actress_picker.pick_by_name(miss_blackberry)
    miss_blackberry.pop('_id', None)

    assert miss_blackberry == {
        'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
        'debut_year': 2015,
        'name': 'Miss Blackberry'
    }

async def test_mark_no_videos(loop, actresses, actress_picker, actress_updater):
    """
    Given actresses,
    When report actress,
    Then actress has_videos flag is false.
    """
    actress = await actress_picker.pick_by_name('Mary Adams')

    actress_name = actress['name']
    await actress_updater.mark_has_videos(actress_name, False)

    actress = await actress_picker.pick_by_name(actress_name)
    assert actress['has_videos'] is False
