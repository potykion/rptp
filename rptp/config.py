import os

from rptp.desktop.data.texts import CANT_FIND_LOGIN_STRING
from rptp.utils.string_utils import split_strip

# DATA
DATA_FOLDER = 'data/'
ACTRESS_BASE_PATH = DATA_FOLDER + 'actresses.json'
SESSION_BASE_PATH = DATA_FOLDER + 'sessions.json'
LOGIN_FILE = DATA_FOLDER + 'login.txt'

# VK
LOGIN = ''
PASSWORD = ''
TOKEN = ''
APP_ID = '4865149'
SCOPE = 'video, offline'
API_VERSION = '5.62'
DEFAULT_SEARCH_PARAMS = {
    'hd': 1,
    'len': 2,
    'notsafe': 1,
    'order': 0,
}

# APP
UPDATE_BASE = True
PICK_ON_START = True
SESSIONS_HTML = 'sessions.html'


def set_up():
    dir_ = os.path.dirname(os.path.relpath(__file__))
    dir_ = os.path.join(dir_, '..')
    os.chdir(dir_)

    os.makedirs(DATA_FOLDER, exist_ok=True)

    _load_login()


def _load_login():
    global LOGIN, PASSWORD, TOKEN

    login_string = 'sample_login, sample_pass'

    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE) as f:
            LOGIN, PASSWORD, TOKEN = split_strip(f.read())
    else:
        login_string = input(CANT_FIND_LOGIN_STRING.format(login_string)).strip(' "')
        LOGIN, PASSWORD = split_strip(login_string)

        from rptp.vk_api import request_token
        TOKEN = request_token()

        with open(LOGIN_FILE, 'w') as f:
            f.write(','.join([LOGIN, PASSWORD, TOKEN]))


set_up()
