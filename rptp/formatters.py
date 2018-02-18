from datetime import timedelta


def format_videos(vk_videos):
    return list(map(format_video, vk_videos))


def format_video(vk_video):
    return {
        'url': 'https://vk.com/video{owner_id}_{id}'.format(**vk_video),
        'mobile_url': 'https://m.vk.com/video{owner_id}_{id}'.format(**vk_video),
        'duration': str(timedelta(seconds=vk_video['duration'])),
        'preview': vk_video['photo_320']
    }
