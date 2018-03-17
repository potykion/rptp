import json
import os

import pytest

from rptp.config import STATIC_DIR
from rptp.models import get_sync_client, upload_actresses, get_async_client, AsyncActressManager
from tests.fixtures import ActressFixtures


@pytest.fixture()
def test_db():
    db_name = 'test'
    yield db_name
    client = get_sync_client()
    client.drop_database(db_name)


@pytest.fixture()
def actresses(test_db):
    with open(os.path.join(STATIC_DIR, 'json', 'actresses.json')) as f:
        actresses_to_upload = json.load(f)
        upload_actresses(actresses_to_upload, test_db)


class TestModels(ActressFixtures):
    async def test_upload_actresses(self, test_db, actresses, async_actress_manager):
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
