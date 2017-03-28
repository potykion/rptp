import time
from functools import wraps
from http.client import ResponseNotReady, CannotSendRequest


def retry_if_http_error(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except(ResponseNotReady, CannotSendRequest):
                time.sleep(2)

    return wrapped
