from rest_framework import authentication, exceptions
from rest_framework.request import Request

from rptp.users.models import User


class VkAcceessTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        try:
            access_token = request.query_params['access_token']
        except KeyError:
            raise exceptions.AuthenticationFailed('No access token passed')

        try:
            user = User.objects.get(access_token=access_token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
