import pytest

from rptp.models import get_sync_client, upload_actresses, get_async_client, AsyncActressManager
from rptp.scrap import parse_debut_page


@pytest.fixture()
def test_db():
    db_name = 'test'
    yield db_name
    client = get_sync_client()
    client.drop_database(db_name)


@pytest.fixture()
def async_actress_manager(test_db):
    client = get_async_client()
    db = client[test_db]
    return AsyncActressManager(db)


async def test_upload_actresses(test_db, async_actress_manager):
    """
    Given parsed actresses,
    When insert them to actress collection,
    Then actress collection contains parsed actresses,
    And Miss Blackberry too.
    """

    parsed_actresses = list(parse_debut_page([2015]))

    upload_actresses(parsed_actresses, test_db)

    assert len(parsed_actresses) == await async_actress_manager.count()

    miss_blackberry = 'Miss Blackberry'
    miss_blackberry = await async_actress_manager.find(miss_blackberry)
    miss_blackberry.pop('_id', None)
    assert miss_blackberry == {
        'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
        'debut_year': 2015,
        'name': 'Miss Blackberry'
    }
