import dj_database_url
from .common import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
