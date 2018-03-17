import json
import os
import pytest

from rptp.config import STATIC_DIR
from rptp.models import get_sync_client, upload_actresses, get_async_client, AsyncActressManager


class ActressFixtures:
    @pytest.fixture()
    def test_db(self):
        db_name = 'test'
        yield db_name
        client = get_sync_client()
        client.drop_database(db_name)

    @pytest.fixture()
    def actresses(self, test_db):
        with open(os.path.join(STATIC_DIR, 'json', 'actresses.json')) as f:
            actresses_to_upload = json.load(f)
            upload_actresses(actresses_to_upload, test_db)

    @pytest.fixture()
    def async_actress_manager(self, test_db):
        client = get_async_client()
        db = client[test_db]
        return AsyncActressManager(db)
