import datetime

from rptp.browser import group_video_timestamps, VideoTimestamp


def test_video_grouping():
    video_timestamps = [
        VideoTimestamp('video-10605510_456245967', False, datetime.datetime(2017, 2, 16, 0, 30, 21, 95827).timestamp()),
        VideoTimestamp('video-10605510_456245967', False, datetime.datetime(2017, 2, 16, 0, 30, 22, 120525).timestamp()),
        VideoTimestamp('video-10605510_456245967', False, datetime.datetime(2017, 2, 16, 0, 30, 23, 147154).timestamp()),
    ]

    grouped_video_timestamps = group_video_timestamps(video_timestamps)

    assert grouped_video_timestamps == {
        'video-10605510_456245967': [
            {
                'from': datetime.datetime(2017, 2, 16, 0, 30, 21, 95827).timestamp(),
                'to': datetime.datetime(2017, 2, 16, 0, 30, 23, 147154).timestamp(),
                'is_playing': False
            }
        ]
    }

    s = 'as'
