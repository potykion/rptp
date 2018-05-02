def test_upload_actresses(actresses, sync_db):
    """
    Given parsed actresses,
    When insert them to actress collection,
    Then actress collection contains parsed actresses,
    And Miss Blackberry too.
    """

    assert len(actresses) == sync_db.actresses.count()

    miss_blackberry = 'Miss Blackberry'
    miss_blackberry = sync_db.actresses.find_one({'name': miss_blackberry})
    miss_blackberry.pop('_id', None)

    assert miss_blackberry == {
        'link': 'http://www.pornteengirl.com/model/miss-blackberry.html',
        'debut_year': 2015,
        'name': 'Miss Blackberry'
    }

