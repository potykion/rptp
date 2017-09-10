import requests


class VkApi:
    URL = 'https://api.vk.com/method'
    VERSION = 5.68

    def __init__(self, access_token):
        self.access_token = access_token
        self.path = []

    def __getattr__(self, item):
        self.path = [*self.path, item]
        return self

    def __call__(self, *args, **kwargs):
        url = f'{VkApi.URL}/{self}'
        response = requests.get(url, params={
            **kwargs,
            'v': VkApi.VERSION,
            'access_token': self.access_token
        })
        return response.json()

    def __str__(self):
        return '.'.join(self.path)


def request_vk_videos(access_token, query, count, offset):
    vk_api = VkApi(access_token)
    default_params = {
        'sort': 0,
        'hd': 1,
        'adult': 1,
        'filters': 'mp4,long',
    }
    vk_response = vk_api.video.search(**default_params, q=query, count=count, offset=offset)
    vk_videos = vk_response['response']['items']
    return vk_videos
