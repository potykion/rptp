import asyncio
import itertools
import logging
from contextlib import closing
from operator import itemgetter

from pymongo.collection import Collection

from rptp.config import VK_TOKEN
from rptp.models import get_db, check_actress_has_videos

# @profile
async def sync_actresses_without_videos(db, token):
    actresses: Collection = db.actresses
    actresses_without_videos = list(actresses.find({"has_videos": False}))

    actresses_without_videos_str = "\n".join(
        map(itemgetter("name"), actresses_without_videos)
    )
    logging.info(f"Actress without videos:\n{actresses_without_videos_str}")

    has_videos_vector = await asyncio.gather(*(
        check_actress_has_videos(actress["name"], token)
        for actress in actresses_without_videos
    ))
    actresses_with_videos = itertools.compress(actresses_without_videos, has_videos_vector)

    actresses_with_videos_ids = list(map(itemgetter("_id"), actresses_with_videos))
    actresses.update_many(
        {"_id": {"$in": actresses_with_videos_ids}}, {"$set": {"has_videos": True}}
    )

    actresses_with_videos_str = "\n".join(
        map(itemgetter("name"), actresses_with_videos)
    )
    logging.info(f"Actress with videos:\n{actresses_with_videos_str}")


async def sync_all_actresses(db, token):
    actresses: Collection = db.actresses

    actresses_with_videos = (
        actress for actress in actresses.find() if actress.get("has_videos", True)
    )

    logging.info("Searching for actress without videos...")

    for actress in actresses_with_videos:
        has_videos = await check_actress_has_videos(actress["name"], token)
        if not has_videos:
            actresses.update_one(
                {"_id": actress["_id"]}, {"$set": {"has_videos": False}}
            )
            logging.info(actress["name"])


if __name__ == "__main__":
    assert VK_TOKEN

    db = get_db()

    with closing(asyncio.get_event_loop()) as loop:
        loop.run_until_complete(sync_actresses_without_videos(db, VK_TOKEN))
