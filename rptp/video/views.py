from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from rptp.users.auth import VkAcceessTokenAuthentication
from rptp.video.serializers import VkVideoSerializer, VkVideoSearchQueryParamsSerializer
from rptp.video.utils import filter_adult_videos
from rptp.vk.utils.api import request_vk_videos


@api_view(['GET'])
@authentication_classes((VkAcceessTokenAuthentication,))
def video_search_view(request: Request):
    """
    Search adult VK videos.

    Args:
        request: Request with query params listed in VkVideoSearchQueryParamsSerializer and access token.

    Returns:
        Response with videos and index of last video for further calls.
    """
    query_params_serializer = VkVideoSearchQueryParamsSerializer(data=request.query_params)
    query_params_serializer.is_valid(raise_exception=True)

    vk_videos = request_vk_videos(
        request.user.access_token,
        **query_params_serializer.validated_data
    )
    vk_videos, offset = filter_adult_videos(
        vk_videos,
        query_params_serializer.validated_data['count']
    )

    serializer = VkVideoSerializer(data=list(vk_videos), many=True)
    serializer.is_valid(raise_exception=True)

    return Response(
        data={
            'videos': serializer.validated_data,
            'offset': offset
        },
        headers={
            'Access-Control-Allow-Origin': '*'
        }
    )
