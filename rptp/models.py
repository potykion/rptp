import asyncio
from itertools import tee
from typing import Dict, Iterable

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.results import InsertManyResult

from rptp.config import MONGO_URL, MONGO_DB, VK_REQUESTS_FREQUENCY
from rptp.getters import get_videos


def get_client():
    return MongoClient(MONGO_URL)


def get_db(db_name=None, client=None) -> Database:
    db_name = db_name or MONGO_DB
    client = client or get_client()
    return client[db_name]


def insert_actresses(
    db: Database, actresses_to_upload: Iterable[Dict]
) -> Iterable[Dict]:
    actresses_to_upload, inserted_actresses = tee(actresses_to_upload)

    result: InsertManyResult = db.actresses.insert_many(actresses_to_upload)

    return [
        {**actress, "id_": id_}
        for actress, id_ in zip(inserted_actresses, result.inserted_ids)
    ]


async def check_actress_has_videos(actress, token):
    videos = await get_videos(actress, token)

    await asyncio.sleep(VK_REQUESTS_FREQUENCY)

    return bool(videos)
