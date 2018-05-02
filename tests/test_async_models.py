from rptp.async_actress import mark_has_videos


async def test_mark_has_videos(loop, actresses, async_db):
    """
    Given actresses,
    When report actress,
    Then actress has_videos flag is false.
    """
    actress_name = 'Mary Adams'

    await mark_has_videos(async_db, actress_name, False)

    actress = await async_db.actresses.find_one({'name': actress_name})
    assert actress['has_videos'] is False
