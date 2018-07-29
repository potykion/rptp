from functools import wraps

from sanic.response import redirect, json

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
            if not token:
                return redirect('/index')

            response = await f(request, *args, **kwargs)
            save_token_data(response, token)
            return response

        return decorated_function

    return decorator


def api_authorization_required():
    """
    Extract token from request, if token not present return error response.
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = extract_auth_data(request)
            if not token:
                return json({'error': 'No authorization token passed.'})

            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator


def required_query_params(params):
    """
    Check {params} exist in query parameters, redirect to index if any parameter is not present.
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if any(parameter not in request.args for parameter in params):
                return redirect('/index')

            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
