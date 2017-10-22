import logging

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from rptp.users.models import User
from rptp.vk.utils.auth import generate_auth_link, receive_token_from_code

logger = logging.getLogger(__name__)


@api_view(['GET'])
def auth_user_view(request: Request):
    code = request.query_params.get('code')

    if code:
        result = receive_token_from_code(code)

        if 'access_token' in result:
            user, _ = User.objects.get_or_create(
                user_id=result['user_id'],
            )
            user.access_token = result['access_token']
            user.save()

            return Response({
                'user_id': result['user_id'],
                'access_token': result['access_token']
            })
        else:
            logger.exception(result)

    return Response(
        {'auth_url': generate_auth_link()}
    )
