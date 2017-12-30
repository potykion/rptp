import logging

from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from rptp.users.auth import update_user_token, VkAcceessTokenAPIAuthentication
from rptp.vk.utils.auth import generate_auth_link, receive_token_from_code

logger = logging.getLogger(__name__)


@api_view(['GET'])
def auth_api_view(request: Request):
    """
    Authorize user via VK.
    Args:
        request: Request with code query parameter.

    Returns:
        Response with:
        - Code-receive link if code is not present in request;
        - Authorization info (token, user_id) otherwise.
    """
    code = request.query_params.get('code')

    if code:
        result = receive_token_from_code(code)

        if 'access_token' in result:
            update_user_token(result['user_id'], result['access_token'])

            return Response({
                'user_id': result['user_id'],
                'access_token': result['access_token']
            })
        else:
            logger.exception(result)

    return Response(
        {'auth_url': generate_auth_link()}
    )


def auth_template_view(request: HttpRequest):
    def _auth(auth_data, request):
        request.session.update(auth_data)
        user = authenticate(request, **auth_data)
        login(request, user)

    if 'access_token' not in request.session:

        # new year local dev hack
        if 'access_token' in request.GET and 'user_id' in request.GET:
            _auth(
                {
                    'user_id': request.GET['user_id'],
                    'access_token': request.GET['access_token']
                },
                request
            )
        else:
            auth_data = auth_api_view(request).data

            if 'auth_url' in auth_data:
                return render(request, 'auth.html', context=auth_data)
            elif 'access_token' in auth_data:
                _auth(auth_data, request)

    return redirect(reverse('client:main'))
