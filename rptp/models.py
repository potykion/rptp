from typing import Dict, Iterable

from pymongo.database import Database


def upload_actresses(
        db: Database,
        actresses_to_upload: Iterable[Dict]
):
    db.actresses.insert_many(actresses_to_upload)
