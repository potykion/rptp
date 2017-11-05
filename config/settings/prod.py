from .common import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = [
    '.herokuapp.com',
]

ADMINS = [('potykion', 'potykion@gmail.com')]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'potykion@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True