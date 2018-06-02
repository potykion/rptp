from rptp.scripts.scrap_ptg import parse_debut_page


def test_parse_debut_page():
    """
    Given debut year,
    When parse debut page,
    And find Miss Blackberry,
    Then Miss Blackberry exists.
    """
    debut_year = 2015
    actresses = parse_debut_page([debut_year])

    miss_blackberry = next(
        actress
        for actress in actresses
        if actress['name'] == 'Miss Blackberry'
    )

    assert miss_blackberry == {
        'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
        'debut_year': 2015,
        'name': 'Miss Blackberry'
    }
