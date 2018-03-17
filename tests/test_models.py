import pytest

from rptp.models import ActressManager, _get_client
from rptp.scrap import parse_debut_page


@pytest.fixture()
def test_db():
    db_name = 'test'
    yield db_name
    client = _get_client()
    client.drop_database(db_name)


@pytest.fixture()
def manager(test_db):
    return ActressManager(test_db)


def test_upload_actresses(manager):
    """
    Given parsed actresses,
    When insert them to actress collection,
    Then actress collection contains parsed actresses,
    And Miss Blackberry too.
    """

    parsed_actresses = list(parse_debut_page([2015]))

    manager.upload_actresses(parsed_actresses)

    assert len(parsed_actresses) == manager.actresses.count()

    miss_blackberry = manager.find_actress('Miss Blackberry')
    assert miss_blackberry == {
        'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
        'debut_year': 2015,
        'name': 'Miss Blackberry'
    }
