from functools import wraps

from sanic.response import redirect

from rptp.auth import extract_auth_data
from rptp.cookie import save_token_data


def browser_authorization_required():
    """
    Extract token from request, if token present save token to cookies, redirect to index otherwise.
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = extract_auth_data(request)

            if token:
                response = await f(request, *args, **kwargs)
                save_token_data(response, token)
                return response
            else:
                return redirect('/index')

        return decorated_function

    return decorator
