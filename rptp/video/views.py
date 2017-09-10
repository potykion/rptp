from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from rptp.video.utils import filter_adult_videos, format_vk_videos
from rptp.vk.utils import request_vk_videos

generate_model = lambda: 'Sasha'


@api_view(['GET'])
def video_search_view(request: Request):
    query = request.query_params.get('q', generate_model())
    count = int(request.query_params.get('count', 30))
    initial_offset = int(request.query_params.get('offset', 0))
    access_token = request.user.access_token

    vk_videos = request_vk_videos(access_token, query, count, initial_offset)
    vk_videos, offset = filter_adult_videos(vk_videos, count)
    videos = format_vk_videos(vk_videos)

    return Response(data={'videos': list(videos), 'offset': offset})
