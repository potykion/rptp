import asyncio
import logging
from contextlib import closing
from operator import itemgetter

from pymongo.collection import Collection

from rptp.config import VK_TOKEN, VK_REQUESTS_FREQUENCY, ENVIRONMENT
from rptp.getters import get_videos
from rptp.models import get_db


async def sync_actresses_without_videos(db, token):
    actresses: Collection = db.actresses
    actresses_without_videos = list(actresses.find({"has_videos": False}))

    actresses_without_videos_str = "\n".join(
        map(itemgetter("name"), actresses_without_videos)
    )
    logging.info(f"Actress without videos:\n{actresses_without_videos_str}")

    actresses_with_videos = [
        actress
        for actress in actresses_without_videos
        if await check_actress_has_videos(actress["name"], token)
    ]

    actresses_with_videos_ids = list(map(itemgetter("_id"), actresses_with_videos))
    actresses.update_many(
        {"_id": {"$in": actresses_with_videos_ids}}, {"$set": {"has_videos": True}}
    )

    actresses_with_videos_str = "\n".join(
        map(itemgetter("name"), actresses_with_videos)
    )
    logging.info(f"Actress with videos:\n{actresses_with_videos_str}")


async def check_actress_has_videos(actress, token):
    videos = await get_videos(actress, token)

    if ENVIRONMENT != "test":
        await asyncio.sleep(VK_REQUESTS_FREQUENCY)

    return bool(videos)


if __name__ == "__main__":
    assert VK_TOKEN

    db = get_db()

    with closing(asyncio.get_event_loop()) as loop:
        loop.run_until_complete(sync_actresses_without_videos(db, VK_TOKEN))
