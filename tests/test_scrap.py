from operator import itemgetter

from rptp.scrap import parse_debut_page


def test_parse_debut_page():
    """
    Given debut page,
    When parse debut page,
    Then actresses with debut year in 1990, 2017 range exists,
    And actress has name, link and debut year,
    And Miss Blackberry exists.
    """
    actresses = list(parse_debut_page())

    miss_blackberry = next(
        actress
        for actress in actresses
        if actress['name'] == 'Miss Blackberry'
    )

    assert set(actresses[0].keys()) == {'debut_year', 'link', 'name'}
    assert set(map(itemgetter('debut_year'), actresses)) == set(range(1990, 2018))
    assert miss_blackberry == {
        'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
        'debut_year': 2015,
        'name': 'Miss Blackberry'
    }
