from rptp.config import MONGO_DB, MONGO_URL


def upload_actresses(actresses_to_upload, db_name=None):
    db = get_db(db_name)
    db.actresses.insert_many(actresses_to_upload)


class AsyncActressManager:
    def __init__(self, db):
        self.actresses = db.actresses

    async def find(self, name):
        return await self.actresses.find_one({'name': name})

    async def pick_random(self, with_id=True):
        actresses = await self.actresses.aggregate(
            [{'$sample': {'size': 1}}]
        ).to_list(1)
        actress = actresses[0]

        if not with_id:
            actress.pop('_id')

        return actress

    async def count(self):
        return await self.actresses.count()


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
