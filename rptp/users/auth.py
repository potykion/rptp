from typing import Tuple, Any

from rest_framework import authentication, exceptions
from rest_framework.request import Request

from rptp.users.models import User


class VkAccessTokenAuthenticationBackend:
    def authenticate(self, request, access_token=None, user_id=None, **kwargs):
        try:
            return User.objects.get(access_token=access_token, user_id=user_id)
        except User.DoesNotExists:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class VkAcceessTokenAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request) -> Tuple[User, Any]:
        """
        Get access token from request, try to find user with such access token.
        Args:
            request: Request with access_token query param / session key.

        Returns:
            Tuple of user and auth object (e.g. token or None).

        """

        access_token = request.query_params.get('access_token', None) or \
                       request.session.get('access_token', None)

        if not access_token:
            raise exceptions.AuthenticationFailed('No access token passed')

        try:
            user = User.objects.get(access_token=access_token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None


def update_user_token(user_id: int, access_token: str) -> User:
    """
    Get or create user by user_id, update its token.
    Args:
        user_id: User id, if no user with such id then new user is created.
        access_token: New token.

    Returns:
        User with updated token.

    """
    user, _ = User.objects.get_or_create(
        user_id=user_id,
    )
    user.access_token = access_token
    user.save()
    return user
