from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from rptp.actress.models import Actress, DEFAULT_ACTRESS
from rptp.users.auth import VkAcceessTokenAPIAuthentication
from rptp.video.serializers import VkVideoSerializer, VideoSearchSerializer
from rptp.video.utils import filter_adult_videos
from rptp.vk.utils.api import request_vk_videos


@api_view(['GET'])
@authentication_classes((VkAcceessTokenAPIAuthentication,))
def video_search_api_view(request: Request):
    """
    Search adult VK videos.

    Args:
        request: Request with query params listed in VkVideoSearchQueryParamsSerializer and access token.

    Returns:
        Response with videos and index of last video for further calls.
    """
    query_params_serializer = VideoSearchSerializer(data=request.query_params)
    query_params_serializer.is_valid(raise_exception=True)

    vk_videos = request_vk_videos(
        request.user.access_token,
        **query_params_serializer.validated_data
    )
    vk_videos, offset = filter_adult_videos(
        vk_videos,
        query_params_serializer.validated_data['count'],
        query_params_serializer.validated_data['offset']
    )

    serializer = VkVideoSerializer(data=vk_videos, many=True)
    serializer.is_valid(raise_exception=True)

    return Response(
        data={
            'videos': serializer.validated_data,
            'offset': offset,
            'query': query_params_serializer.validated_data['query']
        }
    )


@login_required(login_url=reverse_lazy('client:auth'))
def video_search_template_view(request: HttpRequest):
    api_response = video_search_api_view(request)

    query_missed = lambda: api_response.status_code == 400 and 'query' in api_response.data
    no_videos = lambda: not api_response.data.get('videos', None)

    if query_missed() or no_videos():
        actress = Actress.objects.get_random()
        query = actress.name if actress else DEFAULT_ACTRESS
        return redirect('{}?query={}'.format(reverse('client:video:search'), query))

    return render(request, 'video_search.html', api_response.data)
