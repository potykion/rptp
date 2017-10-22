import logging

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from rptp.users.auth import update_user_token
from rptp.vk.utils.auth import generate_auth_link, receive_token_from_code

logger = logging.getLogger(__name__)


@api_view(['GET'])
def auth_user_view(request: Request):
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
