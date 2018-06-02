import logging
from operator import itemgetter

from pymongo.collection import Collection

from rptp.models import get_db
from rptp.scripts import scrap_ptg


def sync_actresses_with_ptg(db):
    ptg_actresses = scrap_ptg.parse_debut_page()

    db_actresses: Collection = db.actresses
    db_actresses_links = frozenset(map(itemgetter("link"), db_actresses.find()))

    new_actresses = [
        actress
        for actress in ptg_actresses
        if actress["link"] not in db_actresses_links
    ]
    new_actresses_str = "\n".join(map(itemgetter("name"), new_actresses))
    logging.info(f"New actresses from ptg:\n{new_actresses_str}")

    db_actresses.insert_many(new_actresses)


if __name__ == "__main__":
    db = get_db()
    sync_actresses_with_ptg(db)
