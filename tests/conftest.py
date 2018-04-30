import json
import json
import os

import pytest

from rptp.app import app
from rptp.config import STATIC_DIR, BASE_DIR, MONGO_DB
from rptp.models import get_sync_client, upload_actresses, get_async_client, AsyncActressManager, ActressPicker, \
    ActressUpdater, get_db


@pytest.fixture
def test_cli(loop, test_client):
    return loop.run_until_complete(test_client(app))


@pytest.fixture()
def mongo_test_db():
    db_name = MONGO_DB
    assert db_name == 'test'

    yield db_name

    client = get_sync_client()
    client.drop_database(db_name)


@pytest.fixture()
def sync_db(mongo_test_db):
    return get_db(mongo_test_db)


@pytest.fixture()
def async_db(mongo_test_db):
    return get_db(mongo_test_db, get_async_client())


@pytest.fixture()
def actresses(sync_db):
    with open(os.path.join(STATIC_DIR, 'json', 'actresses.json')) as f:
        actresses_to_upload = json.load(f)
        upload_actresses(actresses_to_upload, sync_db)
        return actresses_to_upload


@pytest.fixture()
def async_actress_manager(async_db):
    return AsyncActressManager(async_db)


@pytest.fixture()
async def vk_video_response():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)


@pytest.fixture()
async def vk_videos():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)['response']['items']


@pytest.fixture()
async def vk_token_response():
    return {
        "access_token": "32fb57fa0c146de382e9433a48c032e73ca159450460d463987ce9b52943846540c6899af777a49977346",
        "expires_in": 0,
        "user_id": 16231309
    }


@pytest.fixture()
def vk_token():
    return '32fb57fa0c146de382e9433a48c032e73ca159450460d463987ce9b52943846540c6899af777a49977346'


@pytest.fixture()
def vk_user():
    return 16231309


@pytest.fixture()
def vk_video():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_video.json')
    with open(path) as f:
        return json.load(f)


@pytest.fixture()
def actress_picker(async_db):
    return ActressPicker(async_db)


@pytest.fixture()
def actress_updater(async_db):
    return ActressUpdater(async_db)
