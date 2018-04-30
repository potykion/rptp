from rptp.formatters import format_video


def test_video_formatter(vk_video):
    """
    Given vk video,
    When format vk video,
    Then formatted video contains video links, preview, str-duration.
    """
    video = format_video(vk_video)

    assert video == {
        'preview': 'https://pp.userapi.com/c627623/v627623889/49c74/1f_JKV_2jBE.jpg',
        'url': 'https://vk.com/video-81447889_456239209',
        'mobile_url': 'https://m.vk.com/video-81447889_456239209',
        'duration': '0:22:52'
    }
