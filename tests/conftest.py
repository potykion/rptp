import json
import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from rptp.app import app
from rptp.config import STATIC_DIR, BASE_DIR, MONGO_DB, MONGO_URL
from rptp.models import insert_actresses, get_client


@pytest.fixture
def test_cli(loop, test_client):
    return loop.run_until_complete(test_client(app))


@pytest.fixture()
def sync_client():
    return get_client()


@pytest.fixture()
def async_client():
    return AsyncIOMotorClient(MONGO_URL)


@pytest.fixture()
def mongo_test_db(sync_client):
    db_name = MONGO_DB
    assert db_name == 'test'

    yield db_name

    sync_client.drop_database(db_name)


@pytest.fixture()
def sync_db(mongo_test_db, sync_client):
    return sync_client[mongo_test_db]


@pytest.fixture()
def async_db(mongo_test_db, async_client):
    return async_client[mongo_test_db]


@pytest.fixture()
def actresses(sync_db):
    with open(os.path.join(STATIC_DIR, 'json', 'actresses.json')) as f:
        actresses_to_upload = json.load(f)
        return insert_actresses(sync_db, actresses_to_upload)


@pytest.fixture()
def actress_without_videos(sync_db):
    with open(os.path.join(STATIC_DIR, 'json', 'actresses.json')) as f:
        actresses_to_upload = json.load(f)[:5]

        for actress in actresses_to_upload:
            actress['has_videos'] = False

        return insert_actresses(sync_db, actresses_to_upload)


@pytest.fixture()
def vk_video_response():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)


@pytest.fixture()
def vk_videos():
    path = os.path.join(BASE_DIR, 'static', 'json', 'vk_videos_response.json')
    with open(path) as f:
        return json.load(f)['response']['items']


@pytest.fixture()
def vk_token_response():
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
