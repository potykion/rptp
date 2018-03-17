import os

from pymongo import MongoClient

MONGO_URL = os.environ['MONGO_URL']
DEFAULT_DB = 'rptp'


class ActressManager:
    def __init__(self, db_name=None):
        db = _get_db(db_name or DEFAULT_DB)
        self.actresses = db.actresses

    def upload_actresses(self, actresses_to_upload):
        self.actresses.insert_many(actresses_to_upload)

    def find_actress(self, name, with_id=False):
        actress = self.actresses.find({'name': name}).next()

        if not with_id:
            actress.pop('_id')

        return actress


def _get_db(db_name):
    client = _get_client()
    db = client[db_name]
    return db


def _get_client():
    client = MongoClient(MONGO_URL)
    return client
