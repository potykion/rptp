from .common import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = [
    '.herokuapp.com',
]