import os

AUTH_REDIRECT_URI = os.environ.get(
    'VK_AUTH_REDIRECT_URI', 'https://rptp.herokuapp.com/auth'
)

APP_ID = os.environ['VK_APP_ID']
CLIENT_SECRET = os.environ['VK_CLIENT_SECRET']

API_VERSION = os.environ.get('VK_API_VERSION', 5.68)
