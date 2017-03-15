from rptp import Browser


def test_browser_url():
    with Browser() as browser:
        url = browser.current_url
        assert url == 'https://vk.com/feed'
