import logging
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# GENERAL
ENVIRONMENT = os.environ['ENVIRONMENT']

# OS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# VK
APP_ID = os.environ['VK_APP_ID']
CLIENT_SECRET = os.environ['VK_CLIENT_SECRET']
AUTH_REDIRECT_URI = os.environ.get(
    'VK_AUTH_REDIRECT_URI',
    'https://rptp.herokuapp.com/auth'
)
API_VERSION = os.environ.get('VK_API_VERSION', 5.73)
VK_TOKEN = os.getenv('VK_TOKEN')
VK_REQUESTS_FREQUENCY = 1 / 3

# MONGO
MONGO_URL = os.environ['MONGO_URL']
MONGO_DB = os.environ['MONGO_DB']

# LOGGING
logging.getLogger().setLevel(logging.INFO)
