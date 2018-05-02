import re

from motor.motor_asyncio import AsyncIOMotorDatabase


async def pick_random(
        db: AsyncIOMotorDatabase,
        with_id=True
):
    actresses = await db.actresses.aggregate([
        {'$match': {"has_video": {'$ne': False}}},
        {'$sample': {'size': 1}}
    ]).to_list(1)

    actress = actresses[0]

    if not with_id:
        actress.pop('_id')

    return actress


async def mark_has_videos(
        db: AsyncIOMotorDatabase,
        name: str,
        has_videos=True
):
    return await db.actresses.update_one(
        {'name': re.compile(name, re.IGNORECASE)},
        {'$set': {'has_videos': has_videos}}
    )
