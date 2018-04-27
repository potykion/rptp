import re

from rptp.config import MONGO_DB, MONGO_URL


def upload_actresses(actresses_to_upload, db_name=None):
    db = get_db(db_name)
    db.actresses.insert_many(actresses_to_upload)


class AsyncActressManager:
    def __init__(self, db):
        self.actresses = db.actresses

    async def find(self, name):
        return await self.actresses.find_one(
            {'name': re.compile(name, re.IGNORECASE)}
        )

    async def filter(self, **conditions):
        return await self.actresses.aggregate([
            {'$match': conditions},
        ]).to_list()

    async def filter_without_videos(self):
        return await self.filter(has_video=False)

    async def pick_random(self, with_id=True):
        actresses = await self.actresses.aggregate([
            {'$match': {"has_video": {'$ne': False}}},
            {'$sample': {'size': 1}}
        ]).to_list(1)

        actress = actresses[0]

        if not with_id:
            actress.pop('_id')

        return actress

    async def count(self):
        return await self.actresses.count()

    async def mark_has_videos(self, name, has_videos=True):
        return await self.actresses.update_one(
            {'name': re.compile(name, re.IGNORECASE)},
            {'$set': {'has_videos': has_videos}}
        )


def get_db(db_name=None, client=None):
    db_name = db_name or MONGO_DB
    client = client or get_sync_client()
    return client[db_name]


def get_sync_client():
    from pymongo import MongoClient

    return MongoClient(MONGO_URL)


def get_async_client():
    from motor.motor_asyncio import AsyncIOMotorClient

    return AsyncIOMotorClient(MONGO_URL)
