from unittest import mock

import pytest

from rptp.scripts.sync_with_ptg import sync_actresses_with_ptg


@pytest.fixture()
def ptg_new_actresses():
    return [
        {
            "name": "Scarlett Johnson",
            "link": "http://www.pornteengirl.com/model/scarlett-johnson.html",
            "debut_year": 2018,
        },
        {
            "debut_year": 2015,
            "name": "Stefanie",
            "link": "http://www.pornteengirl.com/model/stefanie.html",
        },
    ]


def test_sync_actresses_with_ptg(sync_db, actresses, ptg_new_actresses):
    initial_len = len(actresses)

    with mock.patch(
        "rptp.scripts.scrap_ptg.parse_debut_page", return_value=ptg_new_actresses
    ):
        sync_actresses_with_ptg(sync_db)

    assert sync_db.actresses.count() == initial_len + 1
